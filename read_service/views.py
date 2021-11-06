from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class HealthcheckViewSet(viewsets.ViewSet):

    @action(detail=False)
    def healthcheck(self, request):
        """Perform a healthcheck on the server"""
        return Response(status=status.HTTP_200_OK)
