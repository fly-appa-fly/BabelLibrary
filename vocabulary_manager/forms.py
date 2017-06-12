from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_manager.models import Language, Profile


#     lang_choices = [(c.id, c.eng_name) for c in Language.objects.all()]
#     tag_choices = [(c.id, c.name) for c in Tag.objects.all()]

class AnswerForm(forms.Form):
    choices = forms.ChoiceField()
