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

    def test_get_blog_by_id_success(self):
        blog = BlogFactory(category=self.category)
        response = self.blog_repo.get_by_id(blog.id)
        self.assertTrue(response.success)
        self.assertEqual(response.data.id, blog.id)

    def test_get_blog_by_id_not_found(self):
        response = self.blog_repo.get_by_id(999)
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

    def test_update_blog_success(self):
        blog = BlogFactory(category=self.category)
        response = self.blog_repo.update(
            blog.id,
            title="Updated Title",
            is_published=True
        )
        self.assertTrue(response.success)
        self.assertEqual(response.data.title, "Updated Title")
        self.assertEqual(response.data.slug, "updated-title")

    def test_update_blog_not_found(self):
        response = self.blog_repo.update(999, title="Updated")
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Blog not found")

    def test_delete_blog_success(self):
        blog = BlogFactory(category=self.category)
        response = self.blog_repo.delete(blog.id)
        self.assertTrue(response.success)
        self.assertFalse(Blog.objects.filter(id=blog.id).exists())

    def test_delete_blog_not_found(self):
        response = self.blog_repo.delete(999)
        self.assertFalse(response.success)
        self.assertEqual(response.message, "Blog not found")