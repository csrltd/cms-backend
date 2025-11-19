from loguru import logger
from base.responses import APIResponse
from contact.repository.contact_repository import ContactRepository


class ContactService:
    def __init__(self):
        self.repository = ContactRepository()

    def save_contact_message(self, data):
        try:
            repo_response = self.repository.create(data)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            # Send email notification asynchronously if Celery is available
            self.send_email_notification(repo_response.data)
            
            return APIResponse(True, "Contact message saved successfully", repo_response.data, 201)
        except Exception as e:
            logger.error(f"Error saving contact message: {str(e)}")
            return APIResponse(False, "Failed to save contact message", status=500)

    def send_email_notification(self, contact_message):
        try:
            from contact.tasks import send_email_notification_task
            send_email_notification_task.delay(
                contact_message.full_name,
                contact_message.email,
                contact_message.subject,
                contact_message.message
            )
        except Exception as e:
            logger.warning(f"Failed to queue email notification: {str(e)}")