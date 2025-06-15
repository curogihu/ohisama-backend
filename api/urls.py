from rest_framework.routers import DefaultRouter
from api.views import TVerViewSet  # __init__.pyで読み込まれていればOK

router = DefaultRouter()
# router.register(r'tver', TVerViewSet)
router.register(r'tver', TVerViewSet, basename='tver')

urlpatterns = router.urls