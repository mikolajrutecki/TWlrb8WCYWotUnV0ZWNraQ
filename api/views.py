from rest_framework.viewsets import ModelViewSet

from api.models import Request
from api.serializers import RequestSerializer


class RequestViewSet(ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()
