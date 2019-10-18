from datetime import timedelta

from django.utils import timezone

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import RequestModel, RequestModelResponse
from api.serializers import RequestModelSerializer, RequestModelResponseSerializer


class RequestModelViewSet(ModelViewSet):
    serializer_class = RequestModelSerializer
    queryset = RequestModel.objects.all()

    def create(self, request, *args, **kwargs):
        now = timezone.now()
        serializer = RequestModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req = RequestModel.objects.create(url=request.data['url'],
                                          interval=int(request.data['interval']),
                                          last_run_at=now,
                                          next_run_at=now + timedelta(seconds=int(request.data['interval'])))
        req.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def history(self, request, pk=None):
        request_model = get_object_or_404(RequestModel, id=pk)
        request_model_responses = RequestModelResponse.objects.filter(request_model=request_model)
        serialized_responses = RequestModelResponseSerializer(request_model_responses, many=True)
        serializer_data = serialized_responses.data
        return Response(serializer_data, status=status.HTTP_200_OK)

