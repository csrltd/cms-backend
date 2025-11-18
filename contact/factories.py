import factory
from factory import Faker

from .models import ContactMessage


class ContactMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactMessage

    name = Faker("name")
    email = Faker("email")
    subject = Faker("sentence", nb_words=6)
    message = Faker("paragraph", nb_sentences=3)
