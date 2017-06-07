from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from user_manager.forms import *
from library.models import List
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the library index.")


def detail(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, 'user_manager/detail.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_manager/change_password.html', {
        'form': form
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateForm(data=request.POST, instance=request.user)
        form2 = UpdatePForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and form2.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.save()
            update = form2.save(commit=False)
            update.profile = request.user.profile
            update.save()
            return redirect('/user/' + request.user.username)
    else:
        form = UpdateForm(instance=request.user)
        form2 = UpdatePForm(instance=request.user.profile)

    return render(request, 'user_manager/user_update.html', {'form': form, 'form2': form2})


def sign_up(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.avatar = form.cleaned_data.get('avatar')
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            list = List()
            list.name = 'Reading'
            list.user = user
            list.save()
            list = List()
            list.name = 'For future'
            list.user = user
            list.save()
            list = List()
            list.name = 'Favourite'
            list.user = user
            list.save()
            list = List()
            list.name = 'Finished'
            list.user = user
            list.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'user_manager/sign_up.html', {'form': form})


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('user/login')
    return render(request, 'user_manager/sign_in.html', {})


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')