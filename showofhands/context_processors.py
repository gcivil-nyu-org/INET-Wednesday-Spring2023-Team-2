from chat.models import Connection_Model
from posts.models import Noti_Model


def friend_request_count(request):
    if request.user.is_authenticated:
        count = Connection_Model.objects.filter(
            to_user=request.user, connection_status="Pending"
        ).count()
    else:
        count = 0
    return {"friend_request_count": count}


def tagged_count(request):
    if request.user.is_authenticated:
        count = Noti_Model.objects.filter(
            recipient=request.user, is_read="False"
        ).count()
    else:
        count = 0
    return {"tagged_count": count}
