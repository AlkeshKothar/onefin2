#django imports
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import requests

#rest framework imports
from rest_framework import viewsets, status,generics, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


#local imports
from .serializer import RegisterSerializer, UserSerializer,UserSerializer,GeneresSerializer,MovieSerializer,CollectionSerializer
from movie_app.models import Collections
from movie_app.models import Generes , Movie , Collections 


#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokenr = TokenObtainPairSerializer().get_token(user)  
        tokena = AccessToken().for_user(user)

        return Response({
            #"message": "User Created Successfully.",
            #"refresh" : str(tokenr),
            "access_token" : str(tokena)
        })


#Movie API to view and get data from 3rd party API
class MovieView(APIView):

    def get(self, request, *args, **kwargs):
        #permission_classes = [permissions.IsAuthenticated,]
        page_number = request.GET['page'] if 'page' in request.GET else None
        url = settings.MOVIE_API_URL if not page_number else "{}?page={}".format(settings.MOVIE_API_URL, page_number)
        user = settings.MOVIE_API_USER
        password = settings.MOVIE_USER_PASS
        movie_data = requests.get( url, auth=(user, password)).json()
        if movie_data.get('next') : movie_data['next'] = movie_data['next'].replace(url, request.build_absolute_uri((reverse('movie'))))
        if movie_data.get('previous') : movie_data['previous'] = movie_data['previous'].replace(url, request.build_absolute_uri((reverse('movie'))))
        return Response(movie_data)
    
#Collection API to add movies to custom collection
class CollectionsView(viewsets.ViewSet):

    serializer_class = CollectionSerializer
    """
    Example:

    {
    "title": "Web Series",
    "description" : "all best series",
    "movies": [
        {
            "title": "Dark",
            "description": "A time travel series",
            "genres": [ {"generes_name" : "Time Travel"}, {"generes_name" : "Suspense"}],
            "uuid": "4802ed90-7129-4d53-919f-35c8974b47e6"
        }
    ],
    "created_by": int:enter pk of user
    }

    """
    
    def list(self, request):
        #data = Collections.objects.filter(created_by=request.user)
        data = Collections.objects.all()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)


    def create(self, request):
        # permission_classes = [IsAuthenticated]
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        # permission_classes = [IsAuthenticated]
        data = Collections.objects.get(uuid=pk)
        serializer = self.serializer_class(data)
        return Response(serializer.data)

    def update(self, request, pk=None):
        obj = Collections.objects.get(uuid=pk)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response("Something went wrong",status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        pass
        

    def destroy(self, request, pk=None):
        #permission_classes = [permissions.IsAuthenticated,]
        try:
            data = Collections.objects.get(uuid=pk)
            data.delete()
            return Response("Record Deleted ",status=status.HTTP_200_OK)
        except:
            pass
        return Response("No such records found...",status=status.HTTP_204_NO_CONTENT)


