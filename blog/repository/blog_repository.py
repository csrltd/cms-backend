from django.utils.text import slugify
from loguru import logger
from base.responses import RepositoryResponse
from blog.models import Blog, Category

class BlogRepository:
    def create(self, data):
        try:
            if 'title' in data:
                data['slug'] = slugify(data['title'])
            
            # Validate category exists if category_id is provided
            if 'category_id' in data:
                if not Category.objects.filter(id=data['category_id']).exists():
                    return RepositoryResponse(
                        success=False,
                        message="Category not found"
                    )
            
            blog = Blog.objects.create(**data)
            return RepositoryResponse(
                success=True,
                message="Blog created successfully",
                data=blog
            )
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to create blog: {str(e)}"
            )

    def get_by_slug(self, slug):
        try:
            blog = Blog.objects.select_related('category').get(slug=slug)
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
            logger.error(f"Error retrieving blog {slug}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to retrieve blog: {str(e)}"
            )

    def list_all(self, published_only=False, category_slug=None, date_from=None, date_to=None):
        try:
            queryset = Blog.objects.select_related('category')
            
            if published_only:
                queryset = queryset.filter(is_published=True)
                
            if category_slug:
                queryset = queryset.filter(category__slug=category_slug)
                
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
                
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
                
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

    def update_by_slug(self, slug, **kwargs):
        try:
            blog = Blog.objects.get(slug=slug)
            
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
            logger.error(f"Error updating blog {slug}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to update blog: {str(e)}"
            )

    def delete_by_slug(self, slug):
        try:
            blog = Blog.objects.get(slug=slug)
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
            logger.error(f"Error deleting blog {slug}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to delete blog: {str(e)}"
            )