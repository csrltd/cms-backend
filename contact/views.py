from rest_framework.decorators import api_view
from rest_framework.response import Response
from contact.service.contact_service import ContactService
from contact.serializers import ContactMessageSerializer


@api_view(['POST'])
def contact_create(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        service = ContactService()
        result = service.save_contact_message(serializer.validated_data)
        
        if result.success:
            response_serializer = ContactMessageSerializer(result.data)
            return Response(response_serializer.data, status=result.status)
        else:
            return Response({'error': result.message}, status=result.status)
    
    return Response(serializer.errors, status=400)
