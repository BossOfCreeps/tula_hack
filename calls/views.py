from django.urls import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from calls.filters import CallFilter, MatchFilter
from calls.models import Call, Match
from calls.serializers import CallSerializer, MatchRatingSerializer, MatchSerializer
from chat.models import Notification
from utils.volunteer_selection import volunteer_selection_logic


class CallViewSet(ModelViewSet):
    queryset = Call.objects.select_related("user").all()
    serializer_class = CallSerializer
    filterset_class = CallFilter

    def get_serializer_context(self):
        return super().get_serializer_context() | {"request": self.request}

    def perform_create(self, serializer):
        volunteer_selection_logic(serializer.save())


class MatchViewSet(ModelViewSet):
    queryset = Match.objects.select_related("user", "call__user").all()
    filterset_class = MatchFilter

    def get_serializer_class(self):
        if self.action == "set_rating":
            return MatchRatingSerializer
        return MatchSerializer

    def get_serializer_context(self):
        return super().get_serializer_context() | {"request": self.request}

    def perform_create(self, serializer):
        obj: Match = serializer.save()
        Notification.create_and_send(
            user=obj.call.user,
            title="Найден волонтер",
            text=f'Найден волонтер для заявки "{obj.call}"',
            link=reverse("call_detail", args=[obj.call_id]),
        )

    @action(methods=["post"], detail=True)
    def rating(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        obj: Match = self.get_object()
        obj.set_rating(data["comment"], data["rating"], data["is_success"])
        obj.refresh_from_db()

        return Response(MatchSerializer(obj).data)
