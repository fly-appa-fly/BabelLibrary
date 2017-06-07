from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_manager.models import Language, Profile


class SignUpForm(UserCreationForm):
    choises = tuple(Language.objects.all().values_list())

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    avatar = forms.ImageField(label='User avatar', required=False, help_text='Optional')
    bio = forms.CharField(required=False)
    #native_lang = forms.ChoiceField()
    #learning_langs = forms.MultipleChoiceField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar', 'bio')


class UpdateForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UpdatePForm(forms.ModelForm):
    avatar = forms.ImageField(label='User avatar', required=False, help_text='Optional')
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'bio')