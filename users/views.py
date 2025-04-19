from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import RegistrationSerializer, UserSerializer


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class MeView(RetrieveAPIView):
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
