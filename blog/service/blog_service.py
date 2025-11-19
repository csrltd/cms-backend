from loguru import logger
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
            
            return APIResponse(True, "Blog created successfully", repo_response.data, 201)
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            return APIResponse(False, "Failed to create blog", status=500)

    def update_blog(self, slug, data):
        try:
            repo_response = self.repository.update_by_slug(slug, **data)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            return APIResponse(True, "Blog updated successfully", repo_response.data)
        except Exception as e:
            logger.error(f"Error updating blog {slug}: {str(e)}")
            return APIResponse(False, "Failed to update blog", status=500)

    def delete_blog(self, slug):
        try:
            repo_response = self.repository.delete_by_slug(slug)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=404)
            
            return APIResponse(True, "Blog deleted successfully", status=204)
        except Exception as e:
            logger.error(f"Error deleting blog {slug}: {str(e)}")
            return APIResponse(False, "Failed to delete blog", status=500)

    def list_blogs(self, category_slug=None, date_from=None, date_to=None):
        try:
            repo_response = self.repository.list_all(
                published_only=True,
                category_slug=category_slug,
                date_from=date_from,
                date_to=date_to
            )
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=500)
            
            return APIResponse(True, "Blogs retrieved successfully", repo_response.data)
        except Exception as e:
            logger.error(f"Error listing blogs: {str(e)}")
            return APIResponse(False, "Failed to retrieve blogs", status=500)

    def get_blog(self, slug):
        try:
            repo_response = self.repository.get_by_slug(slug)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=404)
            
            return APIResponse(True, "Blog retrieved successfully", repo_response.data)
        except Exception as e:
            logger.error(f"Error getting blog {slug}: {str(e)}")
            return APIResponse(False, "Failed to retrieve blog", status=500)