from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from utils import caching_service, constants


class TopNReposViewSet(viewsets.ViewSet):

    @action(detail=False)
    def forks(self, request, N):
        """Respond to a top N repos by forks request"""
        repos = caching_service.retrieve_repos(constants.DEFAULT_ORG)
        if repos is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        repos.sort(key=lambda r: r.forks, reverse=True)
        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'forks': r.forks} for i, r in enumerate(repos[:N])])

    @action(detail=False)
    def last_updated(self, request, N):
        """Respond to a top N repos by last_updated request"""
        repos = caching_service.retrieve_repos(constants.DEFAULT_ORG)
        if repos is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        repos.sort(key=lambda r: r.updated_at, reverse=True)
        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'last_updated': r.updated_at} for i, r in enumerate(repos[:N])])

    @action(detail=False)
    def open_issues(self, request, N):
        """Respond to a top N repos by open_issues request"""
        repos = caching_service.retrieve_repos(constants.DEFAULT_ORG)
        if repos is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        repos.sort(key=lambda r: r.open_issues, reverse=True)
        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'open_issues': r.open_issues} for i, r in enumerate(repos[:N])])

    @action(detail=False)
    def stars(self, request, N):
        """Respond to a top N repos by forks request"""
        repos = caching_service.retrieve_repos(constants.DEFAULT_ORG)
        if repos is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        repos.sort(key=lambda r: r.stargazers_count, reverse=True)
        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'stars': r.stargazers_count} for i, r in enumerate(repos[:N])])

    @action(detail=False)
    def watchers(self, request, N):
        """Respond to a top N repos by watchers request"""
        repos = caching_service.retrieve_repos(constants.DEFAULT_ORG)
        if repos is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        repos.sort(key=lambda r: r.watchers_count, reverse=True)
        return Response([{'rank': i + 1,
                          'repo': r.full_name,
                          'watchers': r.watchers_count} for i, r in enumerate(repos[:N])])
