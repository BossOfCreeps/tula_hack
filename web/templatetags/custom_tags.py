from django import template

from calls.models import Call, Match
from organizations.models import Organization
from users.models import User

register = template.Library()


@register.simple_tag
def param_replace(request, **kwargs):
    params = request.GET.copy()
    for key, value in kwargs.items():
        params[key] = value
    return params.urlencode()


@register.simple_tag
def is_organization_admin(user: User, organization: Organization) -> bool:
    return organization.employees.filter(user=user, is_admin=True).exists() if user.is_authenticated else None


@register.simple_tag
def is_call_admin(user: User, call: Call) -> bool:
    return call.user == user if user.is_authenticated else None


@register.simple_tag
def get_user_call_matches(user: User, call: Call) -> list[Match] | None:
    return call.matches.filter(user=user) if user.is_authenticated else None
