import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shakesbeer.settings')

import django
django.setup()

from app.models import Recipe, UtilisedIngredient, Ingredient
from django.contrib.auth.models import User
from random import randint, uniform
from datetime import *

user = User.objects.all()[0]

def populate():

    add_recipe(name='Mojito',
        instructions="Place the limes, mint and sugar into a sturdy highball glass and 'muddle' or mash with the end of a clean rolling pin, to bruise the mint and release the lime juice. Add the ice and pour over the rum. Add soda water to taste and stir well. Garnish with a mint sprig and serve.",
        ingredients=['lime', 'mint leaves', 'sugar', 'rum', 'water', 'mint sprigs']);

    add_recipe(name='Grand Margarita',
        instructions="Fill a shaker with ice. Add Rouge Liqueur, Don Julio Blanco Tequila and lime juice to the shaker. Shake until cold. Strain into a short glass.",
        ingredients=['rouge liqueur', 'tequila', 'lime juice']);

    add_recipe(name='Strawberry Daiquiri',
        instructions="Fill your shaker 3/4 full with cubed ice. Pour in Captain Morgan Original Spiced Gold, sugar syrup, fresh lime juice and 3 chopped strawberries. Shake vigorously for 10 seconds until cold. Strain into a martini glass and garnish with a strawberry.",
        ingredients=['Captain Morgan Original Spiced Gold', 'lime juice', 'sugar syrup', 'strawberries']);

    add_recipe(name='Caipirinha',
        instructions="Cut lime wedges. Add the lime wedges and sugar to a glass. Muddle the lime and sugar. Fill the glass with ice. Pour Captain Morgan Original Spiced Gold into the glass. Stir thoroughly.",
        ingredients=['Captain Morgan Original Spiced Gold', 'sugar', 'lime']);

    add_recipe(name='Mai Tai',
        instructions="Stir all the ingredients together in a jug or shake them in a cocktail shaker. Put a few cubes of ice in a tumbler, pour over the liquid and garnish with a cherry.",
        ingredients=['white rum', 'dark rum', 'triple sec', 'grenadine', 'almond syrup', 'lime', 'cherry']);

    add_recipe(name='Pina colada',
        instructions="Pulse all the ingredients along with a handful of ice in a blender until smooth. Pour into a tall glass and garnish as you like.",
        ingredients=['pineapple juice', 'white rum', 'coconut cream', 'pineapple']);

    add_recipe(name='White Russian',
        instructions="Mix together all the ingredients. Put some ice cubes in a small tumbler and pour the cocktail over the top.",
        ingredients=['vodka', 'kahlua', 'cream']);

    add_recipe(name='Bellini',
        instructions="Put the peach puree in a Champagne flute up to about 1/3 full and slowly top up with Prosecco.",
        ingredients=['peach puree', 'Prosecco']);

    add_recipe(name='Margarita',
        instructions="Put a little salt on a saucer, then wipe the rim of your martini glass with lime juice. Turn the glass upside down in the salt and twist to coat. Stir the ingredients and a little ice together or put them in a cocktail shaker to combine. Strain into a chilled martini glass. Serve with a slice of lime.",
        ingredients=['tequila', 'lime juice', 'triple sec', 'lime', 'salt']);

    add_recipe(name='Drivers\' punch',
        instructions="Put the cranberries into a medium size, rigid freezer container, cover with water (by about 2.5cm), freeze until solid. Mix the cranberry juice in a large jug (about 1.5 litre) with the orange and lime juices. To serve, smash the sheet of frozen cranberries into shards and put in the bottom of eight highball glasses. Put a wedge of lime and orange and a mint sprig in each glass, then pour in the mixed fruit juices and top up with Appletise.",
        ingredients=['cranberries', 'cranberry juice', 'orange juice', 'lime juice', 'lime', 'orange', 'mint sprigs', 'Appletise']);

    # Print what was added
    for recipe in Recipe.objects.all():
        print recipe.name

# Adding methods
def add_recipe(name, instructions, ingredients, user=user, date=datetime.now(),
                picture='/static/images/no-image.png', avgrating=0.0,
                noratings=0):
    recipe = Recipe.objects.get_or_create(name=name, instructions=instructions,
                    defaults={'user' : user, 'date' : date,
                    'picture' : picture, 'avgrating' : uniform(0, 5),
                    'noratings' : randint(1, 100)})[0]
    for ingredient in ingredients:
        ing = add_ingredient(ingredient)
        utilise_ingredient(recipe, ing, amount="Some")
    return recipe

def add_ingredient(name):
    ingredient = Ingredient.objects.get_or_create(name=name)[0]
    return ingredient

def utilise_ingredient(recipe, ingredient, amount):
    utilised_ingredient = UtilisedIngredient.objects.get_or_create(
        recipe=recipe, ingredient=ingredient, amount=amount)[0]
    return utilised_ingredient

# Start execution here!
if __name__ == '__main__':
    print "Starting shakesbeer population script..."
    populate()