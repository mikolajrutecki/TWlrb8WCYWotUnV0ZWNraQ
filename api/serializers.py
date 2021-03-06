from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from api.models import RequestModel, RequestModelResponse


class RequestModelSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = RequestModel
        fields = ['id', 'url', 'interval']


class RequestModelResponseSerializer(ModelSerializer):
    class Meta:
        model = RequestModelResponse
        fields = ['response', 'duration', 'created_at']
