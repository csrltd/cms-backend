from typing import Iterable, Dict, Any

from contact.models import ContactMessage
from contact.serializers import ContactMessageSerializer


def create(data: Dict[str, Any]) -> ContactMessage:

    serializer = ContactMessageSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def list_messages() -> Iterable[ContactMessage]:
    return ContactMessage.objects.all()