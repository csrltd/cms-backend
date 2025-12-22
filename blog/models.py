from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from base.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Blog(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    short_description = models.TextField()
    content = CKEditor5Field('Text', config_name='default')
    thumbnail = models.ImageField(upload_to='blog/thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title