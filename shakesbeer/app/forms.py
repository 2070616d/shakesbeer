from django import forms
from django.contrib.auth.models import User
from app.models import Comment, Recipe

class CommentForm(forms.ModelForm):
    rating = forms.CharField(max_length=500, help_text="What do you think about this recipe?", widget=forms.Textarea )
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment
        fields = ('rating',)

class RecipeForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    instructions = forms.CharField(max_length=1024, widget=forms.Textarea)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Recipe
        fields = ('name','picture','instructions',)
