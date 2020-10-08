#!/usr/bin/env python
# coding: utf8

""" Storage specification. """

from redis import Redis

from . import configuration

storage: Redis = Redis(host=configuration.REDIS_HOST)
""" API storage. """
