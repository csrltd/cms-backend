import factory
from faker import Faker
from django.utils.text import slugify
from blog.models import Category, Blog

fake = Faker()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))

class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    short_description = factory.LazyFunction(lambda: fake.text(max_nb_chars=150))
    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=1000))
    category = factory.SubFactory(CategoryFactory)
    is_published = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=70))