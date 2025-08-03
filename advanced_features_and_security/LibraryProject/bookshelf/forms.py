from django import forms

class BookSearchForm(forms.Form):
    title = forms.CharField(required=False, max_length=100)
