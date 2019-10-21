from django.urls import path, include
from rest_framework import routers

from api.views import RequestModelViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'fetcher', RequestModelViewSet, 'fetcher')

urlpatterns = [
    path('', include(router.urls))
]

