from calls.models import CallStatus, MatchStatus
from chat.models import Notification
from utils import HelpFormat, HelpType


def help_choices(request):
    unread_notifications = (
        Notification.objects.filter(user=request.user, is_viewed=False).count() if request.user.is_authenticated else 0
    )
    return {
        "HelpType": HelpType,
        "HelpFormat": HelpFormat,
        "CallStatus": CallStatus,
        "MatchStatus": MatchStatus,
        "unread_notifications": unread_notifications,
    }
