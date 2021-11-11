import os, requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from json import JSONDecodeError
from pprint import pprint

from utils import caching_service, github_service


class HealthcheckAPIView(APIView):
    """Handles running a healthcheck on the server"""

    def get(self, request, format=None):
        """Run a healthcheck on the server"""
        if not caching_service.is_redis_available():
            return Response({'message': 'Redis cache is not available'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        elif not github_service.is_github_available():
            return Response({'message': 'Github API service is not available'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'message': 'Service ready'},
                status=status.HTTP_200_OK)


class GithubProxyAPIView(APIView):
    """Service proxies Github API endpoints to Github"""

    def get(self, request, format=None, resource=''):
        """Proxy Github API endpoints to Github"""
        response = github_service.proxy_request(resource)

        if response is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            try:
                return Response(response.json(), status=response.status_code)
            except JSONDecodeError:
                return Response(response.text, status=response.status_code)
