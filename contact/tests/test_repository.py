from django.test import TestCase

from . import repository
from factories import ContactMessageFactory


class ContactRepositoryTests(TestCase):
	def test_create_creates_contact_message(self):
		data = {
			"name": "Alice Example",
			"email": "alice@example.com",
			"subject": "Hello",
			"message": "This is a test message.",
		}

		obj = repository.create(data)

		self.assertIsNotNone(obj.pk)
		self.assertEqual(obj.name, data["name"])
		self.assertEqual(obj.email, data["email"])
		self.assertEqual(obj.subject, data["subject"])
		self.assertEqual(obj.message, data["message"]) 

	def test_list_returns_messages_ordered(self):
		first = ContactMessageFactory()
		second = ContactMessageFactory()

		items = list(repository.list_messages())

		# Model Meta ordering uses -created_at, so second should come before first
		self.assertGreater(items.index(second), -1)
		self.assertGreater(items.index(first), -1)
		self.assertEqual(items[0].pk, second.pk)
		self.assertEqual(items[1].pk, first.pk)
