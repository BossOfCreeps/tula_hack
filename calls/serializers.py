from rest_framework import serializers

from calls.models import Call, Match
from users.serializers import UserSerializer


class CallSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        return Call.objects.create(user=self.context["request"].user, **validated_data)

    class Meta:
        model = Call
        fields = "__all__"


class MatchSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    call = CallSerializer(read_only=True)
    call_id = serializers.PrimaryKeyRelatedField(queryset=Call.objects.all(), source="call", write_only=True)

    def create(self, validated_data):
        return Match.objects.create(user=self.context["request"].user, **validated_data)

    class Meta:
        model = Match
        fields = "__all__"


class MatchRatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    text = serializers.CharField(required=False)
    is_success = serializers.BooleanField()
