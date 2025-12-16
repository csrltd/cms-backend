from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.service.account_service import AccountService
from account.serializers import RegisterSerializer, VerifyEmailSerializer, LoginSerializer, ResendOTPSerializer


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        service = AccountService()
        service_response = service.register_user(serializer.validated_data)
        return Response({
            'success': service_response.success,
            'message': service_response.message,
            'data': service_response.data
        }, status=service_response.status)
    
    return Response({
        'success': False,
        'message': 'Invalid data',
        'data': serializer.errors
    }, status=400)


@api_view(['POST'])
def verify_email(request):
    serializer = VerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        service = AccountService()
        service_response = service.verify_email(
            serializer.validated_data['email'],
            serializer.validated_data['otp_code']
        )
        return Response({
            'success': service_response.success,
            'message': service_response.message,
            'data': service_response.data
        }, status=service_response.status)
    
    return Response({
        'success': False,
        'message': 'Invalid data',
        'data': serializer.errors
    }, status=400)


@api_view(['POST'])
def resend_otp(request):
    serializer = ResendOTPSerializer(data=request.data)
    if serializer.is_valid():
        service = AccountService()
        service_response = service.resend_otp(serializer.validated_data['email'])
        return Response({
            'success': service_response.success,
            'message': service_response.message
        }, status=service_response.status)
    
    return Response({
        'success': False,
        'message': 'Invalid data',
        'data': serializer.errors
    }, status=400)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        service = AccountService()
        service_response = service.login_user(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        return Response({
            'success': service_response.success,
            'message': service_response.message,
            'data': service_response.data
        }, status=service_response.status)
    
    return Response({
        'success': False,
        'message': 'Invalid data',
        'data': serializer.errors
    }, status=400)