from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@authentication_classes([TokenAuthentication])  
@permission_classes([IsAuthenticated])  
def chat(request):
    message = request.data.get('message')
    if message:
        return Response({"message": f"Message received: {message}"}, status=200)
    else:
        return Response({"detail": "Invalid token."}, status=401)