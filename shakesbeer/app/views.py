from django.shortcuts import render
from django.http import HttpResponse
from app.models import Recipe, UtilisedIngredient, Comment

def index(request):
    top10recent = Recipe.objects.order_by('-date')[:10]
    top10rating = Recipe.objects.order_by('-avgrating')[:10]
    context_dict = {'top10recent': top10recent, 'top10rating': top10rating}
    return render(request, 'index.html', context_dict)

def view_recipe(request,recipe_name_slug):
    recipe = Recipe.objects.get(slug=recipe_name_slug)
    ingredients = UtilisedIngredient.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe)
    context_dict = {'recipe': recipe, 'ingredients': ingredients, 'comments': comments}
    return render(request, 'recipe.html', context_dict)

# TODO implement
def add_recipe(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)