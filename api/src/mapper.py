#!/usr/bin/env python
# coding: utf8

""" Provide the GenreMapper class. """

import re

from os.path import exists
from typing import Callable, Dict, List

import MeCab
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from . import configuration

SPACE_CHARSET = '_-/,・'
""" Set of chars that aims to be replaced by blank space. """

REMOVE_CHARSET = "():.!$'‘’"
""" Set of chars that aims to be removed. """

wakati = MeCab.Tagger('-Owakati')
""" Japanese parser. """


def normalize(tag: str) -> str:
    """ Normalize the given tag by removing special chars and / or replacing
    them by blank spaces. Assume that the given tag as the following prefixed
    structure : `lang:tag`.

    If the target lang is `ja` then it will performs an additional
    normalization based on `MeCab wakiti` parser.

    Parameters
    ----------
    tag: str
        Tag to be normalized.

    Returns
    -------
    normalized: str
        Normalized tag.

    Notes
    -----
    No value check is performed for error handling. Thus invalid tag will lead
    to IndexError exception.
    """
    lang = tag[:2]
    tag = tag[3:].lower()
    normalized = []
    for c in tag:
        if c in SPACE_CHARSET:
            normalized.append(' ')
        elif c not in REMOVE_CHARSET:
            normalized.append(c)
    normalized = ''.join(normalized)
    if lang == 'ja':
        normalized = wakati.parse(normalized).replace('\n', '').rstrip()
    return f'{lang}:{normalized}'


def get_genre_name(entity: str) -> str:
    """ Extracts the name of the given entity (which is assumed to be a DBPedia
    URI), by removing leading URI part.

    Paramters
    ---------
    entity: str
        Entity to extract name from as DBPedia URI.

    Returns
    -------
    entity_name: str
        Extracted entity name.
    """
    tokens = re.findall(
        r"(?:\w{2}:)?(?:https?:\/\/\w{0,2}.?dbpedia.org\/resource\/)(.+(?!_)[\w\!])(?:$|(_?\(.+\)$))",  # noqa
        entity)
    if len(tokens) == 0:
        return None
    return tokens[0][0]


class GenreMapper(object):
    """ Genre mapper allows to perform genre prediction. """

    instances: Dict = {}
    """ Mapper instances indexed by source and target languages. """

    mappings: pd.DataFrame = None
    """ Taxonomie mapping table loaded from embeddings. """

    tag_per_lang_graph: Dict = {}
    """ Tagset indexed by language. """

    def __init__(
            self,
            sources: List[str],
            target: str,
            tag_provider):
        """ Default constructor. Client should use static factory method
        `get(sources, target)` instead of creating object themselves.

        Parameters
        ----------
        sources: List[str]
            List of source languages to map genre from.
        target: str
            Target language to map genre to.
        """
        self._sources = sources
        self._target = target
        self._mappings = self.get_mappings(sources, target, tag_provider)

    def predict(
            self,
            tags: List[str],
            tfilter: Callable[[str], bool]) -> List[str]:
        """ Computes predictions from mapping table for the given
        tags.

        Parameters
        ----------
        tags: List[str]
            Tag to predict translation for.
        tfilter: Callable[[str], bool]
            A filtering predicate that returns `True` if tag need to be kept.
        Returns
        -------
        predictions: List[str]
            List of filtered prediction tags.
        """
        predictions = (
            self._mappings
                .loc[tags]
                .mean(axis=0)
                .sort_values(ascending=False)
                .index
                .tolist())
        return [tag for tag in predictions if tfilter(tag)]

    @classmethod
    def load_embeddings(cls: type) -> None:
        """ Class factory method that load embeddings data. """
        path = configuration.EMBEDDINGS
        if not exists(path):
            raise IOError(f'Embeddings file {path} not found')
        embeddings = pd.read_csv(path, index_col=0, header=None)
        similarities = cosine_similarity(embeddings.to_numpy())
        cls.mappings = pd.DataFrame(
            similarities,
            index=embeddings.index,
            columns=embeddings.index)

    @classmethod
    def get_mappings(
            cls: type,
            sources: List[str],
            target: str,
            tag_provider) -> pd.DataFrame:
        """ Static factory method that returns mapping table from embeddings.

        Parameters
        ----------
        sources: List[str]
            Source languages to get mapping table for.
        target: str
            Target language to get mapping table for.

        Returns
        -------
        mappings: pandas.DataFrame
            Built mapping table as pandas.DataFrame
        """
        if cls.mappings is None:
            cls.load_embeddings()
        sources_tags = [
            tag
            for source in sources
            for tag in tag_provider(source)]
        target_tags = tag_provider(target)
        mappings = cls.mappings.loc[
            [normalize(tag) for tag in sources_tags],
            [normalize(tag) for tag in target_tags]].to_numpy()
        return pd.DataFrame(
            mappings,
            index=sources_tags,
            columns=target_tags)

    @classmethod
    def get(
            cls: type,
            sources: List[str],
            target: str,
            tag_provider) -> 'GenreMapper':
        """ Static factory method that creates a GenreMapper instance if not
        existing, and returns it for a given (sources, target) languages pair.

        Parameters
        ----------
        sources: List[str]
            List of source languages to map genre from.
        target: str
            Target language to map genre to.

        Returns
        -------
        mapper: GenreMapper
            Requested instance.
        """
        if len(sources) == 0:
            raise ValueError()
        if not isinstance(target, str):
            raise ValueError()
        # TODO: check language support.
        key = '{}#{}'.format('-'.join(sources), target)
        if key not in cls.instances:
            cls.instances[key] = cls(sources, target, tag_provider)
        return cls.instances[key]
