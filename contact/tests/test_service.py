from unittest.mock import patch, MagicMock
from django.test import TestCase
from contact.service.contact_service import ContactService
from contact.tests.factories import ContactMessageFactory


class ContactServiceTest(TestCase):
    def setUp(self):
        self.service = ContactService()
        self.valid_data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }

    @patch.object(ContactService, '__init__', lambda x: None)
    @patch('contact.repository.contact_repository.ContactRepository')
    def test_save_contact_message_success(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        service = ContactService()
        service.repository = mock_repo
        
        contact_message = ContactMessageFactory.build()
        mock_repo.create.return_value = MagicMock(
            success=True,
            data=contact_message
        )
        
        with patch.object(service, 'send_email_notification'):
            result = service.save_contact_message(self.valid_data)
        
        self.assertTrue(result.success)
        self.assertEqual(result.status, 201)
        mock_repo.create.assert_called_once_with(self.valid_data)

    @patch.object(ContactService, '__init__', lambda x: None)
    @patch('contact.repository.contact_repository.ContactRepository')
    def test_save_contact_message_failure(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        service = ContactService()
        service.repository = mock_repo
        
        mock_repo.create.return_value = MagicMock(
            success=False,
            message="Database error"
        )
        
        result = service.save_contact_message(self.valid_data)
        
        self.assertFalse(result.success)
        self.assertEqual(result.status, 400)

    def test_send_email_notification(self):
        """Test email notification method doesn't crash"""
        contact_message = ContactMessageFactory.build()
        
        # Should not raise exception
        try:
            self.service.send_email_notification(contact_message)
            success = True
        except Exception:
            success = False
            
        self.assertTrue(success)