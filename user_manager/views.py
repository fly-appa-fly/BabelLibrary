from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from user_manager.forms import SignUpForm
from library.models import List
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the library index.")


def detail(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
    }
    return render(request, 'user_manager/detail.html', context)

def sign_up(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
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