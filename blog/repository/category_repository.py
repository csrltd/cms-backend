from django.utils.text import slugify
from django.core.cache import cache
from loguru import logger
from base.responses import RepositoryResponse
from blog.models import Category

class CategoryRepository:
    def create(self, data):
        try:
            if 'name' in data:
                data['slug'] = slugify(data['name'])
            
            category = Category.objects.create(**data)
            
            # Clear categories cache
            try:
                cache.delete('categories:all')
                logger.info("Cleared categories cache after creation")
            except Exception:
                pass
            
            return RepositoryResponse(
                success=True,
                message="Category created successfully",
                data=category
            )
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to create category: {str(e)}"
            )

    def get_by_id(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
            return RepositoryResponse(
                success=True,
                message="Category retrieved successfully",
                data=category
            )
        except Category.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="Category not found"
            )
        except Exception as e:
            logger.error(f"Error retrieving category {category_id}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to retrieve category: {str(e)}"
            )

    def list_all(self):
        try:
            # Check cache first (fail gracefully if Redis down)
            try:
                cache_key = 'categories:all'
                cached_categories = cache.get(cache_key)
                if cached_categories:
                    return RepositoryResponse(
                        success=True,
                        message="Categories retrieved successfully (cached)",
                        data=cached_categories
                    )
            except Exception:
                pass  # Continue without cache
            
            # Get from database
            categories = list(Category.objects.all().order_by('name'))
            
            # Try to cache (fail gracefully) - convert to list for caching
            try:
                cache.set(cache_key, categories, timeout=3600)  # 1 hour cache
                logger.info(f"Cached {len(categories)} categories")
            except Exception as e:
                logger.warning(f"Failed to cache categories: {str(e)}")
            
            return RepositoryResponse(
                success=True,
                message="Categories retrieved successfully",
                data=categories
            )
        except Exception as e:
            logger.error(f"Error listing categories: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to list categories: {str(e)}"
            )