#!/usr/bin/env python
# coding: utf8

""" API types and data classes. """

import re
import requests

from typing import Any, Dict, List, Optional

from pydantic import constr

from .storage import storage

EntityId = constr(
    min_length=32,
    max_length=32,
    regex=r'[0-9a-f]{32}\Z')
""" Restricted string type for entity identifier. """

Locale = constr(regex=r'[a-z]{2}\Z')
""" Restricted string type for language locale expression. """


class Language(object):
    """ Language representation as (locale, label) pair. """

    @staticmethod
    def locales() -> List[Locale]:
        """ Find and returns a list of locale from storage.

        Returns
        -------
        locales: List[str]
            List of locale available in storage.
        """
        length = storage.llen('locales')
        return [
            locale.decode()
            for locale in storage.lrange('locales', 0, length)]

    @staticmethod
    def label(locale: Locale) -> str:
        """ Find and returns a label for a given locale.

        Parameters
        ----------
        locale: str
            Locale to get label for.

        Returns
        -------
        label: str
            Label found from storage.

        Raises
        ------
        ValueError
            If no label exist for this locale.
        """
        label = storage.get(f'locale:{locale}')
        if label is None:
            raise ValueError()
        return label.decode()

    @classmethod
    def get(cls: type) -> List[Dict[str, str]]:
        """ Returns all languages from storage.

        Returns
        -------
        languages: List[Dict[str, str]]
            Language as list of language model.
        """
        return [
            {'locale': locale, 'label': cls.label(locale)}
            for locale in cls.locales()]


class Tags(object):
    """ Tag representation. """

    @staticmethod
    def from_uri(entity: str) -> str:
        """ Extracts the name of the given entity (which is assumed to be a
        DBPedia URI), by removing leading URI part.

        Parameters
        ----------
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

    @staticmethod
    def from_locale(locale: str) -> List[str]:
        """ Find all tags from a given locale from storage.

        Parameters
        ----------
        locale: str
            Locale to find tag from.

        Returns
        -------
        tags: List[str]
            List of tags.
        """
        return [
            tag.decode()
            for tag in storage.smembers(f'tags:{locale}')]

    @staticmethod
    def from_entities(eid: EntityId, locale: Locale) -> List[str]:
        """ Find and returns a list of tag for the entity using given locale.

        Parameters
        ----------
        eid: EntityId
            Identifier of the entity to get tags for.
        locale: Locale
            Locale to get tags for.

        Returns
        -------
        tags: List[str]
            List of tag for this (entity, locale) pair
        """
        key = f'{eid}:{locale}:tags'
        length = storage.llen(key)
        return [tag.decode() for tag in storage.lrange(key, 0, length)]


class Entity(object):
    """ Entity representation. """

    QUERY_ENDPOINT = 'wikipedia.org/w/api.php'
    """ Wikipedia API endpoint. """

    QUERY_PARAMETERS = '&'.join((
        'action=query',
        'format=json',
        'formatversion=2',
        'prop=pageimages|pageterms',
        'piprop=thumbnail',
        'pithumbsize=600'))
    """ Wikipedia API parameters. """

    @classmethod
    def find_cover(cls: type, locale: Locale, uri: str) -> Optional[str]:
        """ Try to find a cover image for the given entity by querying
        Wikipedia entity for the specified locale.

        Parameters
        ----------
        locale: str
            Target locale to search cover for.
        uri: str
            Target entity URI to find cover for.

        Returns
        -------
        cover: Optional[str]
            Entity cover image URL if any, `None` otherwise.
        """
        tokens = uri.split('/')
        name = tokens[-1]
        url = (
            f'https://{locale}.{cls.QUERY_ENDPOINT}'
            f'?{cls.QUERY_PARAMETERS}&titles={name}')
        response = requests.get(url)
        if response.status_code == 200:
            payload = response.json()
            if 'query' in payload and 'pages' in payload['query']:
                pages = payload['query']['pages']
                if len(pages) > 0 and 'thumbnail' in pages[0]:
                    thumbnail = pages[0]['thumbnail']
                    if 'source' in thumbnail:
                        return thumbnail['source']
        return None

    @staticmethod
    def name(uri: str) -> str:
        """ Extracts the name of the given entity (which is assumed to be a
        DBPedia URI), by removing leading URI part.

        Paramters
        ---------
        uri: str
            Entity to extract name from as DBPedia URI.

        Returns
        -------
        entity_name: str
            Extracted entity name.
        """
        name = uri[7:]  # Note: remove http://
        if not name.startswith('dbpedia'):
            name = name[3:]  # Note: remove locale
        name = name[21:]  # Note: remove 'dbpedia.org/resource/'.
        name = name.replace('_', ' ')  # Note: replace _ by whitespace.
        return name

    @classmethod
    def get(cls: type, eid: EntityId) -> Dict[str, Any]:
        """ Retrieve entity with identifier from storage.

        Parameters
        ----------
        eid: EntityId
            Unique entity identifier.

        Returns
        -------
        entity: Dict[str, Any]
            Entity as dict with cover and metadata.
        """
        metadata = [{
            'locale': locale,
            'uri': storage.get(f'{eid}:{locale}').decode(),
            'tags': Tags.from_entities(eid, locale)}
            for locale in Language.locales()
            if storage.get(f'{eid}:{locale}') is not None]
        cover = None
        covers = []
        for localized in metadata:
            localized_cover = cls.find_cover(
                localized['locale'],
                localized['uri'])
            if localized['locale'] == 'en':
                cover = localized_cover
            else:
                covers.append(localized_cover)
        if cover is None:
            cover = covers[0]
        return {'metadata': metadata, 'cover': cover}
