from django.utils.text import slugify
from loguru import logger
from base.responses import RepositoryResponse
from blog.models import Blog, Category

class BlogRepository:
    def create(self, title, short_description, content, category_id, thumbnail=None, is_published=False):
        try:
            category = Category.objects.get(id=category_id)
            slug = slugify(title)
            
            blog = Blog.objects.create(
                title=title,
                slug=slug,
                short_description=short_description,
                content=content,
                category=category,
                thumbnail=thumbnail,
                is_published=is_published
            )
            return RepositoryResponse(
                success=True,
                message="Blog created successfully",
                data=blog
            )
        except Category.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="Category not found"
            )
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to create blog: {str(e)}"
            )

    def get_by_id(self, blog_id):
        try:
            blog = Blog.objects.select_related('category').get(id=blog_id)
            return RepositoryResponse(
                success=True,
                message="Blog retrieved successfully",
                data=blog
            )
        except Blog.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="Blog not found"
            )
        except Exception as e:
            logger.error(f"Error retrieving blog {blog_id}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to retrieve blog: {str(e)}"
            )

    def list_all(self, published_only=False):
        try:
            queryset = Blog.objects.select_related('category')
            if published_only:
                queryset = queryset.filter(is_published=True)
            blogs = queryset.order_by('-created_at')
            return RepositoryResponse(
                success=True,
                message="Blogs retrieved successfully",
                data=blogs
            )
        except Exception as e:
            logger.error(f"Error listing blogs: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to list blogs: {str(e)}"
            )

    def update(self, blog_id, **kwargs):
        try:
            blog = Blog.objects.get(id=blog_id)
            
            if 'title' in kwargs:
                blog.title = kwargs['title']
                blog.slug = slugify(kwargs['title'])
            
            for field, value in kwargs.items():
                if field != 'title' and hasattr(blog, field):
                    setattr(blog, field, value)
            
            blog.save()
            return RepositoryResponse(
                success=True,
                message="Blog updated successfully",
                data=blog
            )
        except Blog.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="Blog not found"
            )
        except Exception as e:
            logger.error(f"Error updating blog {blog_id}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to update blog: {str(e)}"
            )

    def delete(self, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
            blog.delete()
            return RepositoryResponse(
                success=True,
                message="Blog deleted successfully"
            )
        except Blog.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="Blog not found"
            )
        except Exception as e:
            logger.error(f"Error deleting blog {blog_id}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to delete blog: {str(e)}"
            )