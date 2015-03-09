from django.contrib import admin
from app.models import *

admin.site.register(Recipe)
admin.site.register(UtilisedIngredient)
admin.site.register(Ingredient)
admin.site.register(Rating)
admin.site.register(Comment)
