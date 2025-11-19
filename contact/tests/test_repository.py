from django.test import TestCase
from contact.repository.contact_repository import ContactRepository
from contact.tests.factories import ContactMessageFactory
from contact.models import ContactMessage


class ContactRepositoryTest(TestCase):
    def setUp(self):
        self.contact_repo = ContactRepository()

    def test_create_contact_message_success(self):
        """Test successful creation of contact message"""
        data = {
            "full_name": "Alice Example",
            "email": "alice@example.com",
            "subject": "Hello",
            "message": "This is a test message."
        }
        
        response = self.contact_repo.create(data)
        
        self.assertTrue(response.success)
        self.assertEqual(response.data.full_name, data["full_name"])
        self.assertEqual(response.data.email, data["email"])
        self.assertEqual(response.data.subject, data["subject"])
        self.assertEqual(response.data.message, data["message"])

    def test_list_contact_messages_success(self):
        """Test successful listing of contact messages"""
        ContactMessageFactory.create_batch(3)
        
        response = self.contact_repo.list_all()
        
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 3)
