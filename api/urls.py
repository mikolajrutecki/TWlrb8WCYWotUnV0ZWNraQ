from rest_framework import routers

from api.views import RequestModelViewSet

router = routers.SimpleRouter()
router.register(r'fetcher', RequestModelViewSet)

urlpatterns = router.urls
