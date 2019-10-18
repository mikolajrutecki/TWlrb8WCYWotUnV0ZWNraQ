from rest_framework.serializers import ModelSerializer
from api.models import RequestModel, RequestModelResponse


class RequestModelSerializer(ModelSerializer):
    class Meta:
        model = RequestModel
        fields = '__all__'


class RequestModelResponseSerializer(ModelSerializer):
    class Meta:
        model = RequestModelResponse
        fields = ['response', 'duration', 'created_at']
