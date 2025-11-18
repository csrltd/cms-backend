from django.utils.text import slugify
from loguru import logger
from base.responses import RepositoryResponse
from blog.models import Category

class CategoryRepository:
    def create(self, name, description=None):
        try:
            slug = slugify(name)
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=description
            )
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
            categories = Category.objects.all().order_by('name')
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