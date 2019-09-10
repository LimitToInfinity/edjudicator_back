from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status

from .decorators import validate_request_data
from .models import HighScore
from .serializers import HighScoreSerializer, TokenSerializer, UserSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
class CreateHighScoresView(LoginRequiredMixin, GenericAPIView):
    """ GET and POST highscores/ """
    queryset = HighScore.objects.all()
    serializer_class = HighScoreSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        new_high_score = HighScore.objects.create(
            user=request.user,
            value=request.data["value"],
        )
        return Response(
            data=HighScoreSerializer(new_high_score).data,
            status=status.HTTP_201_CREATED
        )

class HighScoresDetailView(RetrieveUpdateDestroyAPIView):
    """ GET, PUT, DELETE highscores/:id/ """
    queryset = HighScore.objects.all()
    serializer_class = HighScoreSerializer

    def get(self, request, *args, **kwargs):
        try:
            new_high_score = self.queryset.get(pk=kwargs["pk"])
            return Response(HighScoreSerializer(new_high_score).data)
        except HighScore.DoesNotExist:
            return Response(
                data={
                    "message": "Yo, that High Score with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
        )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            new_high_score = self.queryset.get(pk=kwargs["pk"])
            serializer = HighScoreSerializer()
            updated_high_score = serializer.update(new_high_score, request.data)
            return Response(HighScoreSerializer(updated_high_score).data)
        except HighScore.DoesNotExist:
            return Response(
                data={
                    "message": "Yo, that High Score with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            new_high_score = self.queryset.get(pk=kwargs["pk"])
            new_high_score.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HighScore.DoesNotExist:
            return Response(
                data={
                    "message": "Yo, that High Score with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListHighScoresView(LoginRequiredMixin, ListAPIView):
    """ Provides a GET method handler. """
    queryset = HighScore.objects.all()
    serializer_class = HighScoreSerializer
    permission_classes = (permissions.IsAuthenticated,)

class LoginView(APIView):
    """ POST auth/login/ """
    # This permission class will overide the global permission class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login saves the user's ID in the session, using Django's session framework.
            login(request, user)
            serializer = TokenSerializer(
                data={
                    # Using drf jwt utility functions to generate a token
                    "token": jwt_encode_handler(
                        jwt_payload_handler(user)
                    )
                }
            )
            serializer.is_valid()
            username = user.username
            email = user.email
            token = serializer.data["token"]
            return Response(
                data={
                    "username": username,
                    "email": email,
                    "token": token
                },
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsersView(APIView):
    """ Post auth/register/ """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "Yo, gotta have a username, password, and email to register."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user = authenticate(request, username=username, password=password)
        login(request, user)
        serializer = TokenSerializer(
            data={
                # Using drf jwt utility functions to generate a token.
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            }
        )
        serializer.is_valid()
        token = serializer.data["token"]
        return Response(
            data={
                "username": username,
                "email": email,
                "token": token
            },
            status=status.HTTP_201_CREATED
        )
