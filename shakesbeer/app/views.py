from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)

# TODO implement
def add_recipe(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)