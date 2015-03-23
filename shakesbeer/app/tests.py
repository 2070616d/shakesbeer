from django.test import TestCase
from app.models import Recipe, UtilisedIngredient, Comment, Ingredient, Rating
from django.contrib.auth.models import User
from datetime import *
import time
from django.core.urlresolvers import reverse

def add_recipe(name, user):
    picture='/static/images/no-image.png'
    recipe = Recipe.objects.get_or_create(name=name,instructions="...",
                                  user= user,date=datetime.now(),picture=picture,avgrating=0.0,noratings=0)[0]
    return recipe

def add_rating(recipe, user, score):
    rating = Rating.objects.get_or_create(recipe=recipe,rating=score,user=user)[0]
    return rating



class ModelTests(TestCase):
    def test_recipe(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)
        self.assertEquals(recipe.__unicode__(), recipe.name)
        
    def test_unique_recipe_slug(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)
        self.assertEqual(recipe.slug, 'test-recipetest-user')
        # if recipe is saved again "-1" will be added to the slug
        recipe.save()
        self.assertEqual(recipe.slug, 'test-recipetest-user-1')

    def test_refresh_ratings(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)

        rating1 = add_rating(recipe, user, 5)
        rating2 = add_rating(recipe, user, 4)
        rating3 = add_rating(recipe, user, 2)
        recipe.refreshRatings()
        # number of ratings should be 3
        self.assertEquals(recipe.noratings, 3)
        # average should be 11 / 3 with two decimal digits, 3.37
        self.assertEquals(recipe.avgrating, 3.67)

    def test_ingredient(self):
          ingredient = Ingredient.objects.create(name="ingredient name")
          self.assertEqual(ingredient.__unicode__(), ingredient.name)
          
        

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
        time.sleep(0.5)
        self.assertEqual(top10recent[1], recipe2)
        time.sleep(0.5)
        self.assertEqual(top10recent[2], recipe1)

        top10rating = response.context['top10rating']
        num_popular_recipes = len(top10rating)
        self.assertEqual(num_popular_recipes , 3)

        # check if recipes ar sorted by most ratings
        self.assertEqual(top10rating[0], recipe2)
        self.assertEqual(top10rating[1], recipe1)
        self.assertEqual(top10rating[2], recipe3)

    def test_view_recipe(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)

        response = self.client.get('/shakesbeer/recipe/test-recipetest-user/')
        self.assertEqual(response.context['recipe'], recipe)
        self.assertEqual(response.context['current_rating'], 0)

    def test_get_results(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)
        recipe2 = add_recipe("recipe", user)

        response = self.client.get('/shakesbeer/results/test/')
        results = response.context['results']
        self.assertEquals(len(results), 1)

        recipe = add_recipe("test recipe 2", user)
        response = self.client.get('/shakesbeer/results/test/')
        results = response.context['results']
        self.assertEquals(len(results), 2)

        response = self.client.get('/shakesbeer/results/recipe/')
        results = response.context['results']
        self.assertEquals(len(results), 3)

    def test_results(self):
        user = User.objects.create(username="test user")
        response = self.client.post('/shakesbeer/results/',{'s':'test'})
        results = response.context['results']
        self.assertEquals(len(results), 0)
        
        recipe = add_recipe("test recipe", user)
        recipe2 = add_recipe("recipe", user)
        
        response = self.client.post('/shakesbeer/results/',{'s':'test'})
        results = response.context['results']
        self.assertEquals(len(results), 1)
        similar = response.context['similar']
        self.assertEquals(similar, False)

        response = self.client.post('/shakesbeer/results/',{'s':'recipe'})
        results = response.context['results']
        self.assertEquals(len(results), 2)
        similar = response.context['similar']
        self.assertEquals(similar, False)

        response = self.client.post('/shakesbeer/results/',{'s':['test', 'recipe']})
        results = response.context['results']
        self.assertEquals(len(results), 2)
        similar = response.context['similar']
        self.assertEquals(similar, False)

        response = self.client.post('/shakesbeer/results/',{'s':['test', 'recipe', 'search']})
        results = response.context['results']
        self.assertEquals(len(results), 0)
        similar = response.context['similar']
        self.assertEquals(similar, True)

    def test_get_names(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)
        recipe2 = add_recipe("recipe", user)
        response = self.client.get('/shakesbeer/get_names/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/shakesbeer/get_names/', {'term':'asdfghjkl'})
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertEquals(content, 'fail')
        mimetype = response['Content-Type']
        self.assertEquals(mimetype,'application/json')

        response = self.client.post('/shakesbeer/get_names/', {'term':'recipe'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'test')
        mimetype = response['Content-Type']
        self.assertEquals(mimetype,'application/json')

    def test_get_ingredient_names(self):
        response = self.client.get('/shakesbeer/get_ingredient_names/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/shakesbeer/get_ingredient_names/', {'term':'asdfghjkl'})
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertEquals(content, "fail")
        mimetype = response['Content-Type']
        self.assertEquals(mimetype,'application/json')

        ingredient = Ingredient.objects.create(name="ingredient name")
        ingredient = Ingredient.objects.create(name="test ingredient")
        response = self.client.post('/shakesbeer/get_ingredient_names/', {'term':'ingredient'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'ingredient name')
        self.assertContains(response, 'test ingredient')
        mimetype = response['Content-Type']
        self.assertEquals(mimetype,'application/json')
        

    def test_guest(self):
        response = self.client.get(reverse('addrecipe'))
        self.assertContains(response, 'the glass is empty')

        response = self.client.get(reverse('userpage'))
        self.assertContains(response, 'the glass is empty')

        user = User.objects.create(username="test user")
        recipe = add_recipe("test recipe", user)
        response = self.client.get('/shakesbeer/recipe/test-recipetest-user/')
        self.assertContains(response, 'comment or rate this recipe!')

        response = self.client.get('/shakesbeer/rate/test-recipetest-user/?score=5')
        recipe.refreshRatings()
        self.assertEquals(recipe.avgrating, 0.0)

    def test_invalid_page(self):
        response = self.client.get('/shakesbeer/pagethatdoesntexit/')
        self.assertContains(response,'the glass is empty')

    def test_user_page(self):
        # register user
        response = self.client.post('/accounts/register/', {'username':'bob','email':'bob@bob.com','password1':'password','password2':'password'})
        # log in      
        response = self.client.post('/accounts/login/',{'username':'bob','password2':'password'})
        self.assertEqual(response.status_code, 200)
        # go to user page
        response = self.client.get(reverse('userpage'))
        myrecipes = response.context['myrecipes']
        self.assertEqual(len(myrecipes), 0)

        # add recipes, 2 of which are bob's
        bob = User.objects.get(username="bob")
        user = User.objects.create(username="test user")
        recipe1 = add_recipe('recipe1', bob)
        recipe2 = add_recipe('recipe2', user)
        recipe3 = add_recipe('recipe3', bob)

        # go to user page
        response = self.client.get(reverse('userpage'))
        myrecipes = response.context['myrecipes']
        self.assertEqual(len(myrecipes), 2)

    def test_delete_recipe(self):
        response = self.client.post('/accounts/register/', {'username':'bob','email':'bob@bob.com','password1':'password','password2':'password'})    
        response = self.client.post('/accounts/login/',{'username':'bob','password2':'password'})
        self.assertEqual(response.status_code, 200)
        
        bob = User.objects.get(username="bob")
        recipe = add_recipe('recipe', bob)
        response = self.client.get(reverse('userpage'))
        myrecipes = response.context['myrecipes']
        self.assertEqual(len(myrecipes), 1)

        # delete recipe
        response = self.client.get('/shakesbeer/deleterecipe/recipebob/')
        response = self.client.get(reverse('userpage'))
        myrecipes = response.context['myrecipes']
        self.assertEqual(len(myrecipes), 0)

    def test_rate(self):
        user = User.objects.create(username="test user")
        recipe = add_recipe('test recipe', user)
        response = self.client.post('/accounts/register/', {'username':'bob','email':'bob@bob.com','password1':'password','password2':'password'})    
        response = self.client.post('/accounts/login/',{'username':'bob','password2':'password'})
        response = self.client.get('/shakesbeer/rate/test-recipetest-user/?score=5')
        recipe.refreshRatings()
        self.assertEqual(recipe.avgrating, 5.0)
        # same person changes their rating
        response = self.client.get('/shakesbeer/rate/test-recipetest-user/?score=3')
        recipe.refreshRatings()
        self.assertEqual(recipe.avgrating, 3.0)


    def test_comment(self):
        response = self.client.post('/accounts/register/', {'username':'bob','email':'bob@bob.com','password1':'password','password2':'password'})    
        response = self.client.post('/accounts/login/',{'username':'bob','password2':'password'})
        bob = User.objects.get(username="bob")

        recipe = add_recipe('recipe', bob)
        response = self.client.post('/shakesbeer/recipe/recipebob/', {'rating':'this is a comment'})
        response = self.client.get('/shakesbeer/recipe/recipebob/')
        self.assertContains(response, 'this is a comment')
        
    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'about us')

    def test_login_and_register(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/accounts/register/', {'username':'bob','email':'bob@bob.com','password1':'password','password2':'password'})

        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/accounts/login/',{'username':'bob','password2':'password'})
        
    def test_add_recipe(self):
        # register user
        response = self.client.post('/accounts/register/', {'username':'bob','email':'bob@bob.com','password1':'password','password2':'password'})
        # log in      
        response = self.client.post('/accounts/login/',{'username':'bob','password2':'password'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/shakesbeer/recipe/add/')
        self.assertEqual(response.status_code, 200)
        
        # add recipe from page
        response = self.client.post('/shakesbeer/recipe/add/', {'name':'test recipe','form-0-ingredient':'vodka','form-MIN_NUM_FORMS':'0','form-MAX_NUM_FORMS':'1','form-INITIAL_FORMS':'0','form-TOTAL_FORMS':'1','form-0-amount':'one litre','instructions':'mix','picture':'none'})

        response = self.client.get(reverse('userpage'))
        myrecipes = response.context['myrecipes']
        self.assertEqual(len(myrecipes), 1)
