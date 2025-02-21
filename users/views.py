from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filterset_fields = ["course", "lesson", "payment_method"]
    # filter_backends = [OrderingFilter, DjangoFilterBackend]
    # ordering_fields = ["payment_date"]
