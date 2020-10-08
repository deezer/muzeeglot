#!/usr/bin/env python
# coding: utf8

""" API specification. """

from functools import partial
from os.path import exists
from typing import Any, Dict, List

from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from fastapi.logger import logger
from pydantic import BaseModel, conint
from redis import Redis
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from . import configuration
from .mapper import GenreMapper
from .storage import storage
from .types import Language, Tags, Entity, EntityId

api = FastAPI(docs_url=None, redoc_url=None)
""" API instance. """

index = None
""" Entity name search index. """


class SearchQuery(BaseModel):
    """ Request body model for entity search query. """
    query: str
    sources: List[str]
    target: str
    page: conint(ge=1) = 1


class PredictModel(BaseModel):
    """ Request body model for prediction query. """
    sources: List[str]
    target: str
    eid: EntityId


@api.on_event('startup')
def on_startup():
    """ Callback function for server startup. """
    global index
    if not exists(configuration.INDEX):
        raise IOError('Entity index not found')
    index = open_dir(configuration.INDEX)


@api.get('/heartbeat', status_code=status.HTTP_200_OK)
def heartbeat():
    """ GET / endpoint. """
    pass


@api.get('/languages')
def get_languages() -> List[Dict[str, str]]:
    """ GET /languages endpoint. """
    return Language.get()


@api.get('/entity/{eid}')
def get_entity(eid: EntityId) -> Dict[str, Any]:
    """ GET /entity/{eid} endpoint. """
    return Entity.get(eid)


@api.get('/embeddings')
def get_embeddings() -> FileResponse:
    """ GET /embeddings endpoint. """
    return FileResponse(configuration.REMBEDDINGS)


@api.post('/search')
def search(request: SearchQuery) -> List[Dict[str, Any]]:
    """ POST /search endpoint. """
    clauses = ' OR '.join([f'{source}:1' for source in request.sources])
    clauses = f'{request.target}:1 AND ({clauses})'
    query = request.query.replace("'", ' ')
    query = f"ngram:'{query}' AND {clauses}"
    parser = QueryParser(['ngram'], schema=index.schema)
    query = parser.parse(query)
    with index.searcher() as searcher:
        return [
            {'eid': hit['eid'], 'label': hit['name']}
            for hit in searcher.search_page(query, request.page, pagelen=20)]


@api.post('/predict')
def predict(request: PredictModel) -> List[str]:
    """ GET /predict endpoint. """
    sources = request.sources
    target = request.target
    mapper = GenreMapper.get(sources, target, Tags.from_locale)
    tfilter = partial(storage.sismember, f'tags:{target}')
    predictions = mapper.predict([
        tag
        for source in sources
        for tag in Tags.from_entities(request.eid, source)],
        tfilter)
    return predictions[:10]
