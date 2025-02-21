from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from sales.models import Organization
from sales.serializers import OrganizationSerializer
from users.permissions import IsActive


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_fields = ["country"]
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsActive]
