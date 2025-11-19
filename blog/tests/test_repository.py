from django.test import TestCase
from blog.repository.blog_repository import BlogRepository
from blog.repository.category_repository import CategoryRepository
from blog.tests.factories import CategoryFactory, BlogFactory
from blog.models import Category, Blog

class CategoryRepositoryTest(TestCase):
    def setUp(self):
        self.category_repo = CategoryRepository()

    def test_create_category_success(self):
        data = {
            "name": "Technology",
            "description": "Tech related posts"
        }
        response = self.category_repo.create(data)
        self.assertTrue(response.success)
        self.assertEqual(response.data.name, "Technology")
        self.assertEqual(response.data.slug, "technology")

    def test_get_category_by_id_success(self):
        category = CategoryFactory()
        response = self.category_repo.get_by_id(category.id)
        self.assertTrue(response.success)
        self.assertEqual(response.data.id, category.id)

    def test_get_category_by_id_not_found(self):
        response = self.category_repo.get_by_id(999)
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Category not found")

    def test_list_categories_success(self):
        CategoryFactory.create_batch(3)
        response = self.category_repo.list_all()
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 3)

    def test_create_category_minimal_data(self):
        data = {"name": "Simple Category"}
        response = self.category_repo.create(data)
        self.assertTrue(response.success)
        self.assertEqual(response.data.name, "Simple Category")
        self.assertEqual(response.data.slug, "simple-category")

class BlogRepositoryTest(TestCase):
    def setUp(self):
        self.blog_repo = BlogRepository()
        self.category = CategoryFactory()

    def test_create_blog_success(self):
        data = {
            "title": "Test Blog",
            "short_description": "Test description",
            "content": "Test content",
            "category_id": self.category.id,
            "is_published": True
        }
        response = self.blog_repo.create(data)
        self.assertTrue(response.success)
        self.assertEqual(response.data.title, "Test Blog")
        self.assertEqual(response.data.slug, "test-blog")

    def test_create_blog_invalid_category(self):
        data = {
            "title": "Test Blog",
            "short_description": "Test description",
            "content": "Test content",
            "category_id": 999
        }
        response = self.blog_repo.create(data)
        self.assertFalse(response.success)

    def test_create_blog_minimal_data(self):
        data = {
            "title": "Minimal Blog",
            "content": "Just content",
            "category_id": self.category.id
        }
        response = self.blog_repo.create(data)
        self.assertTrue(response.success)
        self.assertEqual(response.data.title, "Minimal Blog")
        self.assertEqual(response.data.slug, "minimal-blog")

    def test_get_blog_by_slug_success(self):
        blog = BlogFactory(category=self.category)
        response = self.blog_repo.get_by_slug(blog.slug)
        self.assertTrue(response.success)
        self.assertEqual(response.data.slug, blog.slug)

    def test_get_blog_by_slug_not_found(self):
        response = self.blog_repo.get_by_slug('non-existent-slug')
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Blog not found")

    def test_list_blogs_success(self):
        BlogFactory.create_batch(3, category=self.category)
        response = self.blog_repo.list_all()
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 3)

    def test_list_published_blogs_only(self):
        BlogFactory(category=self.category, is_published=True)
        BlogFactory(category=self.category, is_published=False)
        response = self.blog_repo.list_all(published_only=True)
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 1)

    def test_update_blog_by_slug_success(self):
        blog = BlogFactory(category=self.category)
        response = self.blog_repo.update_by_slug(
            blog.slug,
            title="Updated Title",
            is_published=True
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data.title, "Updated Title")
        self.assertEqual(response.data.slug, "updated-title")

    def test_update_blog_by_slug_not_found(self):
        response = self.blog_repo.update_by_slug('non-existent-slug', title="Updated")
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Blog not found")

    def test_delete_blog_by_slug_success(self):
        blog = BlogFactory(category=self.category)
        response = self.blog_repo.delete_by_slug(blog.slug)
        self.assertTrue(response.success)
        self.assertFalse(Blog.objects.filter(slug=blog.slug).exists())

    def test_delete_blog_by_slug_not_found(self):
        response = self.blog_repo.delete_by_slug('non-existent-slug')
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Blog not found")

    def test_list_blogs_filter_by_category(self):
        tech_category = CategoryFactory(slug="technology")
        health_category = CategoryFactory(slug="health")
        BlogFactory.create_batch(2, category=tech_category, is_published=True)
        BlogFactory(category=health_category, is_published=True)
        
        response = self.blog_repo.list_all(published_only=True, category_slug="technology")
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 2)

    def test_list_blogs_filter_by_date_from(self):
        from datetime import datetime, timedelta
        old_blog = BlogFactory(category=self.category, is_published=True)
        old_blog.created_at = datetime.now() - timedelta(days=10)
        old_blog.save()
        
        new_blog = BlogFactory(category=self.category, is_published=True)
        
        date_filter = datetime.now() - timedelta(days=5)
        response = self.blog_repo.list_all(published_only=True, date_from=date_filter)
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 1)

    def test_list_blogs_combined_filters(self):
        from datetime import datetime, timedelta
        tech_category = CategoryFactory(slug="technology")
        health_category = CategoryFactory(slug="health")
        
        # Old tech blog
        old_tech = BlogFactory(category=tech_category, is_published=True)
        old_tech.created_at = datetime.now() - timedelta(days=10)
        old_tech.save()
        
        # New tech blog
        BlogFactory(category=tech_category, is_published=True)
        # New health blog
        BlogFactory(category=health_category, is_published=True)
        
        date_filter = datetime.now() - timedelta(days=5)
        response = self.blog_repo.list_all(
            published_only=True,
            category_slug="technology",
            date_from=date_filter
        )
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 1)