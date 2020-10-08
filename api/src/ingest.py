#!/usr/bin/env python
# coding: utf8

""" Data ingestion script. """

import ast

from os import makedirs
from os.path import exists, join
from typing import Dict
from uuid import uuid4

# pylint: disable=import-error
import pandas as pd

from whoosh.analysis import NgramWordAnalyzer
from whoosh.fields import Schema, BOOLEAN, NGRAMWORDS, STORED
from whoosh.index import create_in
from whoosh.writing import BufferedWriter
# pylint: enable=import-error

from . import configuration
from .storage import storage
from .types import Entity, Language, Tags


def get_tags_corpus() -> Dict:
    """ Corpus loader.

    Returns
    -------
    corpus: Dict
        Tag corpus indexed by identifier and associated locale.
    """
    corpus = {}
    path = join(configuration.DATA, 'corpus.csv')
    df = pd.read_csv(path)
    locales = df.columns[1:]
    for item in df.values:
        eid = item[0]
        corpus[eid] = {}
        for j in range(1, len(item)):
            locale = locales[j - 1]
            if locale not in corpus[eid]:
                corpus[eid][locale] = []
            if isinstance(item[j], str):
                tags = ast.literal_eval(str(item[j]))
                for tag in tags:
                    corpus[eid][locale].append(
                        f'{locale}:{Tags.from_uri(tag)}')
    return corpus


def get_entities_corpus() -> Dict:
    """ Entities loader.

    Returns
    -------
    entities: dict
        Entities URI indexed by identifier and locales.
    """
    entities = {}
    path = join(configuration.DATA, 'entities.csv')
    with open(path, 'r') as stream:
        lines = [line.strip() for line in stream.readlines()]
    for line in lines:
        veid, uri = line.split('\t')
        if veid not in entities:
            entities[veid] = {}
        locale = uri[7:9]
        if locale == 'db':
            locale = 'en'
        entities[veid][locale] = uri
    return entities


def generate_eid() -> str:
    """ Generate and returns a unique identifier for entity. Based of uuid4
    generation and looped until uuid does not exists in storage.

    Returns
    -------
    eid: str
        Generated eid that not exists in storage.
    """
    eid = uuid4().hex
    locales = Language.locales()
    while any([
            storage.get(f'{eid}:{locale}') is not None
            for locale in locales]):
        eid = uuid4().hex
    return eid


def ingest_languages(writer: BufferedWriter):
    print('INFO: start languages ingestion')
    path = join(configuration.DATA, 'languages.csv')
    with open(path, 'r') as stream:
        languages = [line.strip() for line in stream.readlines()]
        for i in range(len(languages)):
            locale, label = languages[i].split(',')
            print(f'\tingest [{locale}] language')
            writer.add_field(locale, BOOLEAN())
            storage.lpush('locales', locale)
            storage.set(f'locale:{locale}', label)


def ingest_tags(corpus: Dict):
    tags = {}
    print('INFO: flatten tags per locale')
    for veid in corpus.keys():
        for locale in corpus[veid].keys():
            if locale not in tags:
                tags[locale] = []
            for tag in corpus[veid][locale]:
                tags[locale].append(tag)
    print('INFO: start tags ingestion')
    for locale in tags.keys():
        print(f'\tingest [{locale}] tags')
        key = f'tags:{locale}'
        for tag in tags[locale]:
            storage.sadd(key, tag)


def ingest_entities(tags_corpus: Dict, writer: BufferedWriter):
    print('INFO: evaluate entities')
    entities_corpus = get_entities_corpus()
    print('INFO: start entities ingestion')
    for veid in entities_corpus.keys():
        if veid not in tags_corpus:
            continue
        tagsets = [
                {'locale': locale, 'values': tags}
                for locale, tags in tags_corpus[veid].items()]
        eid = generate_eid()
        names = set()
        for locale, uri in entities_corpus[veid].items():
            names.add(Entity.name(uri))
            storage.set(f'{eid}:{locale}', uri)
        supported = Language.locales()
        locales = [
            tags['locale']
            for tags in tagsets
            if tags['locale'] in supported and len(tags['values']) > 0]
        onehot = {locale: locale in locales for locale in supported}
        for name in names:
            writer.add_document(
                ngram=name,
                name=name,
                eid=eid,
                **onehot)
        for tags in tagsets:
            locale = tags['locale']
            key = f'{eid}:{locale}:tags'
            for tag in tags['values']:
                storage.lpush(key, tag)


if __name__ == '__main__':
    print('-' * 30)
    print('Muzeeglot data ingestion')
    print('-' * 30)
    if exists(configuration.INGESTION_LOCK):
        print('WARN: ingestion lock detected, pass')
    else:
        print('INFO: evaluate tags corpus')
        tags_corpus = get_tags_corpus()
        print('INFO: create search index')
        if not exists(configuration.INDEX):
            makedirs(configuration.INDEX)
        schema = Schema(ngram=NGRAMWORDS(), name=STORED(), eid=STORED())
        index = create_in(configuration.INDEX, schema)
        writer = BufferedWriter(index, period=60, limit=200)
        ingest_languages(writer)
        ingest_tags(tags_corpus)
        ingest_entities(tags_corpus, writer)
        print('INFO: optimize and close index')
        writer.close()
        index.optimize()
        index.close()
        print('INFO: write ingestion lock')
        with open(configuration.INGESTION_LOCK, 'w') as stream:
            stream.write('ingested')
