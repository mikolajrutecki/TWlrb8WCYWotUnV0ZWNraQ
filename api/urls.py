from rest_framework import routers

from api.views import RequestViewSet

router = routers.SimpleRouter()
router.register(r'fetcher', RequestViewSet)
urlpatterns = router.urls
