from loguru import logger
from django.core.cache import cache
from base.responses import APIResponse
from blog.repository.blog_repository import BlogRepository


class BlogService:
    def __init__(self):
        self.repository = BlogRepository()

    def create_blog(self, data):
        try:
            repo_response = self.repository.create(data)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            # Invalidate cache
            cache.delete('blog_list')
            return APIResponse(True, "Blog created successfully", repo_response.data, 201)
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            return APIResponse(False, "Failed to create blog", status=500)

    def update_blog(self, blog_id, data):
        try:
            repo_response = self.repository.update(blog_id, **data)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            # Invalidate cache
            cache.delete('blog_list')
            return APIResponse(True, "Blog updated successfully", repo_response.data)
        except Exception as e:
            logger.error(f"Error updating blog {blog_id}: {str(e)}")
            return APIResponse(False, "Failed to update blog", status=500)

    def delete_blog(self, blog_id):
        try:
            repo_response = self.repository.delete(blog_id)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=404)
            
            # Invalidate cache
            cache.delete('blog_list')
            return APIResponse(True, "Blog deleted successfully", status=204)
        except Exception as e:
            logger.error(f"Error deleting blog {blog_id}: {str(e)}")
            return APIResponse(False, "Failed to delete blog", status=500)

    def list_blogs(self):
        try:
            # Check cache first
            cached_blogs = cache.get('blog_list')
            if cached_blogs:
                return APIResponse(True, "Blogs retrieved from cache", cached_blogs)
            
            repo_response = self.repository.list_all(published_only=True)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=500)
            
            # Cache the results
            cache.set('blog_list', repo_response.data, 300)  # 5 minutes
            return APIResponse(True, "Blogs retrieved successfully", repo_response.data)
        except Exception as e:
            logger.error(f"Error listing blogs: {str(e)}")
            return APIResponse(False, "Failed to retrieve blogs", status=500)

    def get_blog(self, blog_id):
        try:
            repo_response = self.repository.get_by_id(blog_id)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=404)
            
            return APIResponse(True, "Blog retrieved successfully", repo_response.data)
        except Exception as e:
            logger.error(f"Error getting blog {blog_id}: {str(e)}")
            return APIResponse(False, "Failed to retrieve blog", status=500)