import unittest
from unittest.mock import Mock, patch
from blog.service.blog_service import BlogService
from blog.tests.factories import BlogFactory, CategoryFactory
from base.responses import RepositoryResponse


class TestBlogService(unittest.TestCase):
    def setUp(self):
        self.service = BlogService()
        self.service.repository = Mock()

    def test_create_blog_success(self):
        blog_data = BlogFactory.build()
        self.service.repository.create.return_value = RepositoryResponse(
            True, "Blog created", blog_data
        )
        
        result = self.service.create_blog(blog_data)
        
        self.assertTrue(result.success)
        self.assertEqual(result.status, 201)
        self.service.repository.create.assert_called_once_with(blog_data)

    def test_create_blog_failure(self):
        blog_data = BlogFactory.build()
        self.service.repository.create.return_value = RepositoryResponse(
            False, "Creation failed"
        )
        
        result = self.service.create_blog(blog_data)
        
        self.assertFalse(result.success)
        self.assertEqual(result.status, 400)

    def test_update_blog_success(self):
        blog_data = {'title': 'Updated Title', 'content': 'Updated content'}
        mock_blog = BlogFactory.build()
        self.service.repository.update_by_slug.return_value = RepositoryResponse(
            True, "Blog updated", mock_blog
        )
        
        result = self.service.update_blog('test-slug', blog_data)
        
        self.assertTrue(result.success)
        self.assertEqual(result.status, 200)

    def test_delete_blog_success(self):
        self.service.repository.delete_by_slug.return_value = RepositoryResponse(
            True, "Blog deleted"
        )
        
        result = self.service.delete_blog('test-slug')
        
        self.assertTrue(result.success)
        self.assertEqual(result.status, 204)

    def test_list_blogs_success(self):
        blog_data = [BlogFactory.build()]
        self.service.repository.list_all.return_value = RepositoryResponse(
            True, "Blogs retrieved", blog_data
        )
        
        result = self.service.list_blogs()
        
        self.assertTrue(result.success)
        self.assertEqual(result.data, blog_data)

    def test_list_blogs_failure(self):
        self.service.repository.list_all.return_value = RepositoryResponse(
            False, "Database error"
        )
        
        result = self.service.list_blogs()
        
        self.assertFalse(result.success)
        self.assertEqual(result.status, 500)

    def test_get_blog_success(self):
        blog_data = BlogFactory.build()
        self.service.repository.get_by_slug.return_value = RepositoryResponse(
            True, "Blog found", blog_data
        )
        
        result = self.service.get_blog('test-slug')
        
        self.assertTrue(result.success)
        self.assertEqual(result.data, blog_data)