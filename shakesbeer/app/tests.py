from django.test import TestCase
from app.models import Recipe, UtilisedIngredient, Comment, Ingredient, Rating
from django.contrib.auth.models import User
from datetime import *

def add_recipe(name, user):
    picture='/static/images/no-image.png'
    recipe = Recipe.objects.get_or_create(name=name,instructions="...",
                                  user= user,date=datetime.now(),picture=picture,avgrating=0.0,noratings=0)[0]
    return recipe

def add_rating(recipe, user, score):
    rating = Rating.objects.get_or_create(recipe=recipe,rating=score,user=user)[0]
    return rating

class RecipeModelTests(TestCase):
    def test_slug(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)
        self.assertEqual(recipe.slug, 'test-recipetest-user')
        # if recipe is saved again "-1" will be added to the slug
        recipe.save()
        self.assertEqual(recipe.slug, 'test-recipetest-user-1')

    def test_ratings(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe 2", user)

        rating1 = add_rating(recipe, user, 5)
        rating2 = add_rating(recipe, user, 4)
        rating3 = add_rating(recipe, user, 2)
        recipe.refreshRatings()
        # number of ratings should be 3
        self.assertEquals(recipe.noratings, 3)
        # average should be 3.67
        self.assertEquals(recipe.avgrating, 3.67)
