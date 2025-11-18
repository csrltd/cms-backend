from typing import Iterable, Dict, Any

from .models import ContactMessage
from .serializers import ContactMessageSerializer


def create(data: Dict[str, Any]) -> ContactMessage:
    """Create and return a ContactMessage instance from validated data.

    Uses the serializer for validation.
    """
    serializer = ContactMessageSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def list_messages() -> Iterable[ContactMessage]:
    """Return an iterable of ContactMessage ordered by newest first."""
    return ContactMessage.objects.all()
