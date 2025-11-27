from django.urls import path
from blog.views import category_list, category_detail

urlpatterns = [
    path('categories/', category_list, name='category-list'),
    path('categories/<slug:slug>/', category_detail, name='category-detail'),
]