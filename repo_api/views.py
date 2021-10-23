from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from github import Github
import os
from pprint import pprint


class RepoRankViewSet(viewsets.ViewSet):
    @action(detail=False)
    def forks(self, request, N):
        token = os.getenv('GITHUB_TOKEN')
        ghub = Github(token)
        org = ghub.get_organization('parse-community')
        repos = [repo for repo in org.get_repos()]
        repos.sort(key=lambda r: r.forks_count, reverse=True)
        return Response([{'repo_name': r.full_name,
                          'forks_count': r.forks_count} for r in repos[:N]])
