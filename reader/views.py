from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from library.models import Book
from django import template
from dictionary_manager.models import Word
from vocabulary_manager.models import VocabularyWord

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
        # app_id = '17103d8c'
        # app_key = 'f21dbbc42b922a35c295f67b81459774'
        # language = 'en'
        # url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()
        #
        # r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        #
        # url = 'https://od-api.oxforddictionaries.com:443/api/v1/morphology/' + language + '/' + word.lower()
        #
        # r1 = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        word = word.lower()
        word_object = []
        words = Word.objects.filter(word__contains=word)
        for w in words:
            if (word == w.word) or (word == w.word+'s') or (word == w.word+'es') or (word == w.word+'d') or (word == w.word+'ed'):
                word_object.append(w)
        data = ''
        if word_object is not []:

            for defins in word_object.definitions.all().order_by('pk'):
                data += defins.type + ' <br>'
                for defin in defins.definitions.all().order_by('pk'):
                    data +=  defin.definition + ' <br>'
                data += ' <br>'
        else:
            data = word + " isn't in the dictionary"
    else:
        data = ''
    minitype = 'application/json'
    return HttpResponse(data)

@login_required
@csrf_exempt
def add_word(request, word):
    print('sssss')
    if request.is_ajax():
        word = word.lower()
        word_object = None
        words = Word.objects.filter(word__contains=word)
        for w in words:
            if (word == w.word) or (word == w.word+'s') or (word == w.word+'es') or (word == w.word+'d') or (word == w.word+'ed'):
                word_object = w
                break
        data = ''
        if word_object is not None and len(word_object.vocabularyword_set.filter(user=request.user)) == 0:
            vocab_word = VocabularyWord()
            vocab_word.word = word_object
            vocab_word.user = request.user
            vocab_word.state = 0.
            vocab_word.language = word_object.language
            vocab_word.save()
    print('ddddd')
    return HttpResponse('done')