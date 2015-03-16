from django.shortcuts import render
from django.http import HttpResponse
from app.models import Recipe, UtilisedIngredient, Comment
from app.forms import CommentForm, RecipeForm
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
def addrecipe(request):
    if not request.user.is_authenticated():
        return HttpResponse("You cannot do this as you are not logged in.")
    context_dict={}
    form = RecipeForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.date = datetime.now()
            if 'picture' in request.FILES:
                recipe.picture = request.FILES['picture']
            recipe.save()
        else:
            # The supplied form contained errors - just print them to the terminal.
            context_dict['errors'] = form.errors
    else:
        form = RecipeForm()
    context_dict['form'] = form
    return render(request, 'addrecipe.html', context_dict)

# TODO implement
def results(request):
    results = Recipe.objects.order_by('-date')[:10]
    context_dict = {'results': results}
    return render(request, 'results.html', context_dict)

def about(request):
    return render(request, 'about.html')