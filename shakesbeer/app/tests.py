from django.test import TestCase
from app.models import Recipe, UtilisedIngredient, Comment, Ingredient, Rating
from django.contrib.auth.models import User
from datetime import *
from django.core.urlresolvers import reverse
from django.test.client import Client


AUTHENTICATION_BACKENDS = ["app.auth_backends.TestcaseUserBackend"]

def add_recipe(name, user):
    picture='/static/images/no-image.png'
    recipe = Recipe.objects.get_or_create(name=name,instructions="...",
                                  user= user,date=datetime.now(),picture=picture,avgrating=0.0,noratings=0)[0]
    return recipe

def add_rating(recipe, user, score):
    rating = Rating.objects.get_or_create(recipe=recipe,rating=score,user=user)[0]
    return rating

class TestcaseUserBackend(object):
    def authenticate(self, testcase_user=None):
        return testcase_user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)

class ModelTests(TestCase):
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
        # average should be 11 / 3 with two decimal digits, 3.37
        self.assertEquals(recipe.avgrating, 3.67)

class ViewTests(TestCase):
    def test_index(self):
        user = User.objects.create(username="test user")
        recipe1 = add_recipe("test recipe 1", user)
        recipe2 = add_recipe("test recipe 2", user)
        recipe3 = add_recipe("test recipe 3", user)

        # add ratings to each recipe
        rating1 = add_rating(recipe1, user, 3)
        rating2 = add_rating(recipe2, user, 4)
        rating3 = add_rating(recipe3, user, 1)
        recipe1.refreshRatings()
        recipe2.refreshRatings()
        recipe3.refreshRatings()

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        top10recent = response.context['top10recent']
        num_recent_recipes =len(top10recent)
        self.assertEqual(num_recent_recipes , 3)

        # check if recipes are sorted by most recent
        self.assertEqual(top10recent[0], recipe3)
        self.assertEqual(top10recent[1], recipe2)
        self.assertEqual(top10recent[2], recipe1)

        top10rating = response.context['top10rating']
        num_popular_recipes = len(top10rating)
        self.assertEqual(num_popular_recipes , 3)

        # check if recipes ar sorted by most ratings
        self.assertEqual(top10rating[0], recipe2)
        self.assertEqual(top10rating[1], recipe1)
        self.assertEqual(top10rating[2], recipe3)

##    def test_userpage(self):
##        user = User.objects.create(username="test user", email="test@mail.com", password="1234")
##        user2 = User.objects.create(username="test user 2")
##
##        recipe1 = add_recipe("test recipe 1", user)
##        recipe2 = add_recipe("test recipe 2", user2)
##        recipe3 = add_recipe("test recipe 3", user)
##
##        c = Client()
##        login = c.login(testcase_user=user)
##        self.assertTrue(login)
##        response = self.client.get(reverse('userpage'))
##
##        myrecipes = response.context['myrecipes']
##        num_recipes = len(myrecipes)
##        self.assertEqual(num_recipes, 2)
        
