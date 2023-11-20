from django import forms
from .models import CommentLeet, CommentThoughts


class EmailLeetForm(forms.Form):
    name = forms.CharField(max_length=200)
    sender = forms.EmailField()
    receiver = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)

class CommentLeetForm(forms.ModelForm):
    class Meta:
        model = CommentLeet
        fields = ['name', 'email', 'content']

class EmailThoughtsForm(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.EmailField()
    receiver = forms.EmailField()
    purpose = forms.CharField(max_length=350)
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)

class CommentThoughtsForm(forms.ModelForm):
    class Meta:
        model = CommentThoughts
        fields = ['name', 'email', 'content']

class SearchForm(forms.Form):
    query = forms.CharField()

