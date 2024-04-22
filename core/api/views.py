from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializer import UserSerializer
from rest_framework import generics

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
       
        user = authenticate(username=username, password=password)
        if user is not None:
            data= self.serializer_class(user).data
           
            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)
