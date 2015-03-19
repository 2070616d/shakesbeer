from django.test import TestCase
from app.models import Recipe, UtilisedIngredient, Comment, Ingredient, Rating
from django.contrib.auth.models import User
from datetime import *

class RecipeMethodTests(TestCase):      
    def test_slug(self):
        user = User.objects.create(username="username")
        instructions = "..."
        date = datetime.now()
        picture='/static/images/no-image.png'
        recipe = Recipe.objects.get_or_create(name="test recipe",instructions=instructions,
                                      user= user,date=date,picture=picture,avgrating=0.0,noratings=0)[0]
        self.assertEqual(recipe.slug, 'test-recipeusername')

    def test_unique_slug(self):
        user = User.objects.create(username="username")
        instructions = "..."
        date = datetime.now()
        picture='/static/images/no-image.png'
        recipe = Recipe.objects.get_or_create(name="test recipe",instructions=instructions,
                                      user= user,date=date,picture=picture,avgrating=0.0,noratings=0)[0]
        # if recipe is saved again "-1" will be added to the slug
        recipe.save()
        self.assertEqual(recipe.slug, 'test-recipeusername-1')
