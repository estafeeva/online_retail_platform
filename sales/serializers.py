import rest_framework.serializers
from rest_framework.serializers import ModelSerializer
from sales.models import Organization


class OrganizationSerializer(ModelSerializer):
    debt = rest_framework.serializers.ReadOnlyField()

    class Meta:
        model = Organization
        fields = "__all__"
