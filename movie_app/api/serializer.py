#django imports
from django.contrib.auth.models import User

#rest framework imports
from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated

#local imports
from movie_app.models import Collections, Generes, Movie

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],password = validated_data['password'])
        return user


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Generes serializer
class GeneresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generes
        fields = '__all__'


# Movie serializer
class MovieSerializer(serializers.ModelSerializer):
    genres = GeneresSerializer(many=True)
    class Meta:
        model = Movie
        fields = '__all__'


# Collections serializer
class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    class Meta:
        model = Collections
        #fields = ('title','description','movies','description')
        fields = '__all__'

    def validate_movies(self, movie_obj):
        errors = []
        for movie in movie_obj:
            single_error = {}
            if not movie.get('title'):
                single_error['title'] = 'Title is required'
            if not movie.get('description'):
                single_error['description'] = 'Description is required'
            if not movie.get('genres'):
                single_error['genres'] = 'Genres is required'
            if single_error:
                errors.append(single_error)
        if errors:
            raise serializers.ValidationError(errors)
        return movie_obj

    def create(self, validated_data):
        all_movies = []
        movies_data = validated_data.pop('movies')
        for movie in movies_data:
            all_gener = []
            geners_data = movie.pop('genres')
            for each_geners in geners_data:
                obj, created = Generes.objects.get_or_create(**each_geners)
                all_gener.append(obj)
            obj, created = Movie.objects.get_or_create(**movie)
            obj.genres.add(*all_gener)
            obj.save()
            all_movies.append(obj)
        collection_obj, created = Collections.objects.get_or_create(**validated_data)
        collection_obj.movies.add(*all_movies)
        return collection_obj

 
 

        

       
        
        
        