from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from library.models import Book
from django import template

import requests
import json

def index(request):
    return HttpResponse("Hello, world. You're at the library index.")


def open_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book
    }
    return render(request, 'reader/viewer.html', context)


def get_word(request, word):
    if request.is_ajax():
        app_id = '17103d8c'
        app_key = 'f21dbbc42b922a35c295f67b81459774'
        language = 'en'
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()

        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

        url = 'https://od-api.oxforddictionaries.com:443/api/v1/morphology/' + language + '/' + word.lower()

        r1 = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

        data = r.text + "\n" + r1.text
    else:
        data = 'fail'
    minitype = 'application/json'
    return HttpResponse(data)