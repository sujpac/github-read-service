from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class RepoRankViewSet(viewsets.ViewSet):
    @action(detail=False)
    def forks(self, request, N):
        return Response({'method': 'GET', 'request': request.GET, 'N': N})
