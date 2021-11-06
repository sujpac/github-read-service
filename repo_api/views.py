from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings
from rest_framework import status
from django.core.cache import cache

from redis import Redis, ConnectionError
import logging

from github import Github
from pprint import pprint
from urllib.parse import urlparse
import os, json, pickle


class RepoRankViewSet(viewsets.ViewSet):

    @action(detail=False)
    # @method_decorator(cache_page(settings.CACHE_TTL))
    def forks(self, request, N):
        """Handle a top N repositories by forks request"""
        # pprint('MAKING A GITHUB REQUEST!')
        token = os.getenv(settings.API_KEY_NAME)
        ghub = Github(token)
        org = ghub.get_organization(settings.ORG_NAME)
        print(cache._server)
        redis_url = urlparse(cache._server)
        print(redis_url.hostname, redis_url.port)

        r = Redis(host=redis_url.hostname, port=redis_url.port)
        logging.basicConfig()
        logger = logging.getLogger('redis-log')
        try:
            r.ping()
        except ConnectionError:
            logger.error("Redis isn't running. Try 'redis-server'")

        pickled_org = pickle.dumps(org)
        r.set('org', pickled_org, ex=60*5)
        unpacked_org = pickle.loads(r.get('org'))
        pprint(unpacked_org)
        print(org.public_repos)
        print(unpacked_org == org)
        print(r.ttl('org'))

        repos = [repo for repo in org.get_repos()]
        repos.sort(key=lambda r: r.forks_count, reverse=True)

        pickled_repos = pickle.dumps(repos)
        r.set('repos', pickled_repos, ex=60*5)
        unpacked_repos = pickle.loads(r.get('repos'))
        print(unpacked_repos)
        print(unpacked_repos == repos)
        print(r.ttl('repos'))

        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'num_forks': r.forks_count} for i, r in enumerate(repos[:N])])

    @action(detail=False)
    @method_decorator(cache_page(settings.CACHE_TTL))
    def last_updated(self, request, N):
        """Handle a top N by last_updated request"""
        token = os.getenv(settings.API_KEY_NAME)
        ghub = Github(token)
        org = ghub.get_organization('parse-community')
        repos = [repo for repo in org.get_repos()]
        repos.sort(key=lambda r: r.updated_at, reverse=True)
        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'last_updated': r.updated_at} for i, r in enumerate(repos[:N])])
