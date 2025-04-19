import django_filters

from calls.models import Call, Match, MatchStatus
from users.models import User
from utils import HelpFormat, HelpType


class CallFilter(django_filters.FilterSet):
    class Meta:
        model = Call
        fields = "__all__"


class MatchFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=HelpType.choices, field_name="call__type")
    format = django_filters.ChoiceFilter(choices=HelpFormat.choices, field_name="call__format")
    status = django_filters.ChoiceFilter(choices=MatchStatus.choices)
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.all(), field_name="call__user")
    rating = django_filters.NumberFilter(lookup_expr="gte")

    class Meta:
        model = Match
        fields = "__all__"
