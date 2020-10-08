#!/usr/bin/env python
# coding: utf8

""" Simple configuration factory with envvar binding. """

from os import environ
from os.path import join


DATA: str = environ.get('DATA', '/opt/muzeeglot/data')
""" Default data directory path. """

EMBEDDINGS: str = environ.get(
    'EMBEDDINGS',
    join(DATA, 'embeddings.csv'))
""" Path of the embedding file to load. """

REMBEDDINGS: str = environ.get(
    'REMBEDDINGS',
    join(DATA, 'embeddings_reduced.csv'))
""" Path of the reduced embedding file to load. """

INDEX: str = environ.get('INDEX_DIRECTORY', '/opt/muzeeglot/indexes/search')
""" Path of the search index directory. """

INGESTION_LOCK: str = join(INDEX, 'ingestion.lock')
""" Path of data lock. """

REDIS_HOST: str = environ.get('REDIS_HOST', 'redis')
""" Hostname for Redis storage. """
