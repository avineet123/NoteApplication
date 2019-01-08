from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import status
from knox.models import AuthToken

from .serializers import (NoteSerializer, CreateUserSerializer,
                          UserSerializer, LoginUserSerializer)


##Restict access to authenticated users only.
class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

##Here we validate the user input and create an account if the validation passes.
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })

##Here We create LoginApi.
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })

##We will use this API to determine if the user is logged in and retrieve their token for performing user specific api calls.
##Below API will return user data for the authenticated user or 404  errors if the user is not authenticated or the token is incorrect.
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

#Here we create logout api
class Logout(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self,request,format=None):
        request.user.auth_token.delete()
        return Response(status=204)
