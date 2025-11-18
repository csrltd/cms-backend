from rest_framework import serializers
from .models import Category, Blog

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']

class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'short_description', 'content', 'thumbnail', 
                 'category', 'category_id', 'is_published', 'created_at', 'updated_at']

class BlogListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'short_description', 'thumbnail', 'category', 'created_at']