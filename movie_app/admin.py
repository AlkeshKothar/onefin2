from django.contrib import admin

#local model imports
from .models import Generes, Movie, Collections


# registering models
admin.site.register(Generes)
admin.site.register(Movie)
admin.site.register(Collections)