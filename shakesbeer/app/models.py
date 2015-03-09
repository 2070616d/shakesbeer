from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(User)
    picture = models.ImageField(blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='UtilisedIngredient')

    def __unicode__(self):
        return self.name

    def hasIngredient(self,ingredient):
        for i in self.ingredients.all():
            if i == ingredient:
                return True
        return False

# django canny store dictionaries inside models, therefore we do stupid things like this
class UtilisedIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=64)

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(User)
    rating = models.IntegerField()

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(User)
    rating = models.CharField(max_length=500)