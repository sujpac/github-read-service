import os, requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from pprint import pprint

from utils import caching_service, github_service


class HealthcheckAPIView(APIView):
    """Handles running a healthcheck on the server"""

    def get(self, request, format=None):
        """Run a healthcheck on the server"""
        if caching_service.is_redis_running():
            return Response({'message': 'Service ready'},
                status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Redis cache is down'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GithubProxyAPIView(APIView):
    """Service proxies Github API endpoints to Github"""

    def get(self, request, format=None, resource=''):
        """Proxy Github API endpoints to Github"""
        response = github_service.send_get_request(resource)
        return Response(response.json())
