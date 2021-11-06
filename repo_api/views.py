from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings
from rest_framework import status

from github import Github
import os
from pprint import pprint

cache = {}


class RepoRankViewSet(viewsets.ViewSet):

    @action(detail=False)
    # @method_decorator(cache_page(settings.CACHE_TTL))
    def forks(self, request, N):
        """Handle a top N repositories by forks request"""
        # pprint('MAKING A GITHUB REQUEST!')
        token = os.getenv(settings.API_KEY_NAME)
        ghub = Github(token)
        org = ghub.get_organization('parse-community')
        repos = [repo for repo in org.get_repos()]
        cache[request.path] = org.raw_data
        print(cache[request.path])
        repos.sort(key=lambda r: r.forks_count, reverse=True)
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
