from django.core.exceptions import ObjectDoesNotExist
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

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def history(self, request, pk=None):
        """
        Gets response history for given RequestModel instance id

        :param request: request
        :param pk: id of RequestModel instance
        :return: serialized data
        """
        try:
            request_model = RequestModel.objects.get(id=pk)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request_model_responses = RequestModelResponse.objects.filter(request_model=request_model)
        serialized_responses = RequestModelResponseSerializer(request_model_responses, many=True)
        serializer_data = serialized_responses.data
        return Response(serializer_data, status=status.HTTP_200_OK)

