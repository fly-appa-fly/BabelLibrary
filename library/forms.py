from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from user_manager.models import Language, Profile
from .models import Book, Tag, Author
from user_manager.models import Language
from django.forms import ModelForm

# class BookForm(forms.ModelForm):
#     lang_choices = [(c.id, c.eng_name) for c in Language.objects.all()]
#     tag_choices = [(c.id, c.name) for c in Tag.objects.all()]
#
#     title = forms.CharField(max_length=300)
#     first_name = forms.CharField(max_length=200)
#     last_name = forms.CharField(max_length=200)
#     tags = forms.MultipleChoiceField(choices=tag_choices)
#     language = forms.ChoiceField(choices=lang_choices)
#     cover = forms.ImageField(required=False)
#     content = forms.FileField()
#     annotation = forms.CharField(max_length=10000)
#     private = forms.BooleanField(required=False)
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'tags', 'language', 'cover', 'content', 'annotation', 'private')

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name')