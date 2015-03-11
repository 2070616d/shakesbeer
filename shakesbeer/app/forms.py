from django import forms
from django.contrib.auth.models import User
from app.models import Comment

class CommentForm(forms.ModelForm):
    rating = forms.CharField(max_length=500, help_text="What do you think about this recipe?", widget=forms.Textarea )

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment
        fields = ('rating',)