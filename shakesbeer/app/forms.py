from django import forms
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from app.models import Comment, Recipe, UtilisedIngredient

class CommentForm(forms.ModelForm):
    rating = forms.CharField(max_length=500, help_text="What do you think about this recipe?", widget=forms.Textarea )
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment
        fields = ('rating',)

class UtilisedIngredientForm(forms.Form):
    ingredient = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'what do we need?'}))
    amount = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'how much do we need?'}))

UtilisedIngredientFormSet = formset_factory(UtilisedIngredientForm)

class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    instructions = forms.CharField(max_length=1024, widget=forms.Textarea)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    ings = UtilisedIngredientFormSet()

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Recipe
        fields = ('name','picture','instructions',)
