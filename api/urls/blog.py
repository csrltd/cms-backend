from django.urls import path
from blog.views import blog_list_create, blog_detail

urlpatterns = [
    path('blogs/', blog_list_create, name='blog-list-create'),
    path('blogs/<int:pk>/', blog_detail, name='blog-detail'),
]