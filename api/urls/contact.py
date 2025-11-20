from django.urls import path
from contact.views import contact_create

urlpatterns = [
    path('contact/', contact_create, name='contact-create'),
]