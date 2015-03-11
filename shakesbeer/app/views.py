from django.shortcuts import render
from django.http import HttpResponse
from app.models import Recipe, UtilisedIngredient, Comment
from app.forms import CommentForm
from datetime import *

def index(request):
    top10recent = Recipe.objects.order_by('-date')[:10]
    top10rating = Recipe.objects.order_by('-avgrating')[:10]
    context_dict = {'top10recent': top10recent, 'top10rating': top10rating}
    return render(request, 'index.html', context_dict)

def view_recipe(request,recipe_name_slug):
    recipe = Recipe.objects.get(slug=recipe_name_slug)
    ingredients = UtilisedIngredient.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe)
    # A HTTP POST?
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.date = datetime.now()
            comment.save()
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        form = CommentForm()
    context_dict = {'recipe': recipe, 'ingredients': ingredients, 'comments': comments, 'form': form}
    return render(request, 'recipe.html', context_dict)

# TODO implement
def add_recipe(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)