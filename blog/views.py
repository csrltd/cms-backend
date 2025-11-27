from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.service.blog_service import BlogService
from blog.serializers import BlogSerializer, BlogListSerializer, CategorySerializer
from blog.models import Category


@api_view(['GET', 'POST'])
def blog_list_create(request):
    service = BlogService()
    if request.method == 'GET':
        # Extract optional query parameters
        category_slug = request.GET.get('category')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        service_response = service.list_blogs(
            category_slug=category_slug,
            date_from=date_from,
            date_to=date_to
        )
        if service_response.success:
            serializer = BlogListSerializer(service_response.data, many=True)
            return Response(serializer.data, status=200)
        return Response({
            'success': service_response.success,
            'message': service_response.message
        }, status=service_response.status)
        
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'Authentication required'
            }, status=401)
        
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            service_response = service.create_blog(serializer.validated_data)
            if service_response.success:
                response_serializer = BlogSerializer(service_response.data)
                return Response(response_serializer.data, status=service_response.status)
            return Response({
                'success': service_response.success,
                'message': service_response.message
            }, status=service_response.status)
        
        return Response({
            'success': False,
            'message': 'Invalid data',
            'data': serializer.errors
        }, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, slug):
    service = BlogService()
    if request.method == 'GET':
        service_response = service.get_blog(slug)
        if service_response.success:
            serializer = BlogSerializer(service_response.data)
            return Response(serializer.data, status=200)
        return Response({
            'success': service_response.success,
            'message': service_response.message
        }, status=service_response.status)
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'Authentication required'
            }, status=401)
        
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            service_response = service.update_blog(slug, serializer.validated_data)
            if service_response.success:
                response_serializer = BlogSerializer(service_response.data)
                return Response(response_serializer.data, status=200)
            return Response({
                'success': service_response.success,
                'message': service_response.message
            }, status=service_response.status)
        
        return Response({
            'success': False,
            'message': 'Invalid data',
            'data': serializer.errors
        }, status=400)
    
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': 'Authentication required'
            }, status=401)
        
        service_response = service.delete_blog(slug)
        if service_response.success:
            return Response(status=service_response.status)
        return Response({
            'success': service_response.success,
            'message': service_response.message
        }, status=service_response.status)


@api_view(['GET'])
def category_list(request):
    """List all categories"""
    categories = Category.objects.all().order_by('name')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, slug):
    """Get category details with its blogs"""
    try:
        category = Category.objects.get(slug=slug)
        category_data = CategorySerializer(category).data
        
        # Get published blogs in this category
        blogs = category.blogs.filter(is_published=True).order_by('-created_at')
        blogs_data = BlogListSerializer(blogs, many=True).data
        
        return Response({
            'category': category_data,
            'blogs': blogs_data,
            'blog_count': len(blogs_data)
        })
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)


