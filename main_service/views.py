from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from utils import caching

class HealthcheckViewSet(viewsets.ViewSet):

    @action(detail=False)
    def healthcheck(self, request):
        """Perform a healthcheck on the server"""
        if caching.is_redis_running():
            return Response({'message': 'Service ready'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Redis is down'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
