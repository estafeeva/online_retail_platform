from sales.apps import SalesConfig
from rest_framework import routers

from sales.views import OrganizationViewSet

app_name = SalesConfig.name

router = routers.DefaultRouter()
router.register(r"", OrganizationViewSet, basename="organization")

urlpatterns = []
urlpatterns += router.urls
