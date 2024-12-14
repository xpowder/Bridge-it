from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ProfileSerializer, UserSerializer
from .models import UserProfile
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication



@api_view(['POST'])  
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    if request.method == "POST":
        return Response({"message": "Token is valid!", "user": request.user.username})
    

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "message": "Validation failed","errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"success": False,"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)  
    except User.DoesNotExist:
        return Response({"success": False,"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if user.check_password(password):  
        login(request, user) 
        token, _ = Token.objects.get_or_create(user=user) 
        return Response({"success": True, "message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"success": False,"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
        logout(request)
        return Response({"success": True,'message': 'Logout successful'}, status=status.HTTP_200_OK)
    return Response({ "success": False,'error': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"success": False,"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        email = request.data.get('email')
        if email and email != user.email:
            user.email = email 
            user.save() 
        
        if request.method == "GET":
            serializer = ProfileSerializer(profile)  
            return Response(serializer.data)
        
        elif request.method == "PUT":
            if not request.data:
                return Response({"succes": False, "error":"No data provided"})
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True,"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"success": False,"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
