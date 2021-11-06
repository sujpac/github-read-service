from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from utils import caching


class HealthcheckAPIView(APIView):
    """Handles running a healthcheck on the server"""

    def get(self, request, format=None):
        """Run a healthcheck on the server"""
        if caching.is_redis_running():
            return Response({'message': 'Service ready'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Redis cache is down'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GithubProxyAPIView(APIView):
    """Service proxies Github API endpoints to Github"""

    def get(self, request, format=None, resource=None):
        """Proxy Github API endpoints to Github"""
        
        return Response({"message": resource})
