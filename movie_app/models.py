#django imports
from django.db import models
from django.contrib.auth.models import User

#third party imports
import uuid

class Generes(models.Model):
    generes_name = models.CharField( primary_key=True, max_length=100) 


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    genres = models.ManyToManyField(Generes, null=True)
    uuid = models.UUIDField(primary_key=True)


class Collections(models.Model):
    uuid = models.UUIDField(primary_key=True, default = uuid.uuid4)
    title = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie)
    description = models.CharField(max_length=50)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
  

class CollectionsGener(models.Model):
    pass