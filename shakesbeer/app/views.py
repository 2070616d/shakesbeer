from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app.models import Recipe, UtilisedIngredient, Comment, Ingredient, Rating
from django.db.models import Q
from app.forms import *
from datetime import *
import re
import json
from django.contrib.auth.decorators import login_required

def index(request):
    top10recent = Recipe.objects.order_by('-date')[:10]
    top10rating = Recipe.objects.order_by('-avgrating')[:10]
    context_dict = {'top10recent': top10recent, 'top10rating': top10rating}
    return render(request, 'index.html', context_dict)

def userpage(request):
    current_user = request.user
    myrecipes = Recipe.objects.filter(user=current_user).order_by('-avgrating')
    context_dict = {'myrecipes': myrecipes}
    return render(request, 'userpage.html', context_dict)

def view_recipe(request,recipe_name_slug):
    recipe = Recipe.objects.get(slug=recipe_name_slug)
    ingredients = UtilisedIngredient.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe)

    # update recipe ratings
    recipe.refreshRatings()

    # get user's rating for recipe if available
    current_rating = 0
    if request.user.is_authenticated():
        current_rating = Rating.objects.filter(recipe=recipe,user=request.user)
        if current_rating.exists():
            current_rating = getattr(current_rating[0], 'rating')
        else:
            current_rating = 0

    # A HTTP POST?
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.date = datetime.now()
            comment.save()
            return HttpResponseRedirect('')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        form = CommentForm()
    context_dict = {'recipe': recipe, 'ingredients': ingredients, 'comments': comments, 'form': form, 'current_rating': current_rating}
    return render(request, 'recipe.html', context_dict)

# TODO implement
def addrecipe(request):
    if not request.user.is_authenticated():
        return HttpResponse("You cannot do this as you are not logged in.")
    context_dict={}
    form = RecipeForm()
    #ings = UtilisedIngredientForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        ings = UtilisedIngredientFormSet(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.date = datetime.now()
            if 'picture' in request.FILES:
                recipe.picture = request.FILES['picture']
            else:
                recipe.picture = '/static/images/no-image.png'
            recipe.save()
            print request.POST
            for ing in ings:
                try:
                    if ing.is_valid() and ing.cleaned_data['ingredient']!='':
                        print ing.cleaned_data['ingredient']
                        ingredient=Ingredient.objects.get_or_create(name=ing.cleaned_data['ingredient'])[0]
                        UtilisedIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=ing.cleaned_data['amount'])
                except:
                    pass
            url = '/shakesbeer/recipe/' + recipe.slug + '/'
            return redirect(url)
        else:
            # The supplied form contained errors - just print them to the terminal.
            context_dict['errors'] = form.errors
    else:
        form = RecipeForm()
        #ings = UtilisedIngredientForm()

    context_dict['form'] = form
    #context_dict['ings'] = ings
    return render(request, 'addrecipe.html', context_dict)

def results(request,tag=""):
    results = []
    similar = False

    if request.method == 'POST':
        search = request.POST['s']
    else:
        search = tag

    result = get_results(request, search)
    context_dict = {'results': result['results'][:30], 'similar': result['similar']}

    return render(request, 'results.html', context_dict)


def search(request):
    if request.method == 'GET':
        query = request.GET['search'].strip()

    result = get_results(request, query)

    context_dict = {'results': result['results'][:30], 'similar': result['similar']}

    return render(request, 'search.html', context_dict)

def get_results(request, query):
    results = []
    similar = False

    # Split the string to the list without spaces and commas
    search = re.split(' |, |,', query)
    search = filter(None, search)

    first_term = search[0]
    end_search = search[1:]
    # Filter by first term
    results = Recipe.objects.filter(Q(utilisedingredient__ingredient__name__icontains=first_term) | Q(name__icontains=first_term)).order_by('-avgrating').distinct()

    # # Filter further if more than one word ingredient or name provided
    # # order should preserve
    for s in end_search:
        results = results.filter(Q(utilisedingredient__ingredient__name__icontains=s) | Q(name__icontains=s))

    # If no results exist, find similiar ones
    # i.e. with at least one elemet from search input
    if not results:
        similar = True
        search_regex = r'{0}'.format('|'.join(search))
        results = Recipe.objects.filter(Q(utilisedingredient__ingredient__name__in=search) | Q(name__regex=search_regex)).order_by('-avgrating').distinct()

    context_dict = {'results': results[:30], 'similar': similar}
    return context_dict

def get_names(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        ingredients = Ingredient.objects.filter(name__icontains = q )[:20]
        recipes = Recipe.objects.filter(name__icontains = q)[:10]
        results = []
        for ingredient in ingredients:
            ingredient_json = {}
            ingredient_json['id'] = ingredient.id
            ingredient_json['label'] = ingredient.name
            ingredient_json['value'] = ingredient.name
            results.append(ingredient_json)
        for recipe in recipes:
            recipe_json = {}
            recipe_json['id'] = recipe.id
            recipe_json['label'] = recipe.name
            recipe_json['value'] = recipe.name
            results.append(recipe_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def about(request):
    return render(request, 'about.html')

@login_required
def rate(request,recipe_name_slug):
    recipe = Recipe.objects.get(slug=recipe_name_slug)
    url = '/shakesbeer/recipe/' + recipe_name_slug + '/'
    if request.method == 'GET':
        if 'score' in request.GET:
            score = request.GET['score']
            try:
                rating = Rating.objects.filter(recipe=recipe,user=request.user)
                if rating.exists():
                    rating[0].delete()
                rating = Rating.objects.get_or_create(recipe=recipe, rating=score, user=request.user)[0]
            except:
                pass
    return redirect(url)

@login_required
def deleterecipe(request, recipe_name_slug):
    recipe = Recipe.objects.get(slug=recipe_name_slug)
    url = '/shakesbeer/userpage/'
    currentuser = request.user
    if currentuser == recipe.user:
        recipe.delete()
    return redirect(url)
