from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializer import RegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from user_app import models

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data={}

        if serializer.is_valid():
            account=serializer.save()
            data['response']='Registration Successful'
            data['username']=account.username
            data['email']=account.email

            token=Token.objects.get(user=account).key
            data['token']=token
        else:
            data=serializer.errors    

        return Response(data)
        

        #     username = serializer.validated_data.get('username')
        #     email = serializer.validated_data.get('email')
        #     password = serializer.validated_data.get('password')
        #     password2 = serializer.validated_data.get('password2')

        #     if password != password2:
        #         return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        #     if User.objects.filter(username=username).exists():
        #         return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        #     if User.objects.filter(email=email).exists():
        #         return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        #     user = User.objects.create_user(username=username, email=email, password=password)
        #     user.save()

        #     token, created = Token.objects.get_or_create(user=user)

        #     return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)