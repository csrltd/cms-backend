import factory
from faker import Faker
from contact.models import ContactMessage

fake = Faker()


class ContactMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactMessage

    full_name = factory.LazyFunction(lambda: fake.name())
    email = factory.LazyFunction(lambda: fake.email())
    subject = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    message = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
