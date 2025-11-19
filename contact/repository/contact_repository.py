from loguru import logger
from base.responses import RepositoryResponse
from contact.models import ContactMessage


class ContactRepository:
    def create(self, data):
        try:
            contact_message = ContactMessage.objects.create(**data)
            return RepositoryResponse(
                success=True,
                message="Contact message created successfully",
                data=contact_message
            )
        except Exception as e:
            logger.error(f"Error creating contact message: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to create contact message: {str(e)}"
            )

    def list_all(self):
        try:
            messages = ContactMessage.objects.all().order_by('-created_at')
            return RepositoryResponse(
                success=True,
                message="Contact messages retrieved successfully",
                data=messages
            )
        except Exception as e:
            logger.error(f"Error listing contact messages: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to list contact messages: {str(e)}"
            )