from rest_framework.serializers import ModelSerializer
from api.models import Request


class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
