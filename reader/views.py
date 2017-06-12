import simplejson as simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
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
    if book.private and request.user != book.publisher:
        return redirect('/')
    context = {
        'book': book
    }
    return render(request, 'reader/viewer.html', context)


def get_word(request, word):
    if request.is_ajax():
        word = word.lower()
        word_object = None
        words = Word.objects.filter(word=word)

        for i in range(4):
            if i == 0:
                words = Word.objects.filter(word=word)
            else:
                words = Word.objects.filter(word=word[:-i])
            if len(words) != 0:
                break
        data = ''
        for w in words:
            for defins in w.definitions.all().order_by('pk'):
                data += defins.type + ' <br>'
                for defin in defins.definitions.all().order_by('pk'):
                    data += defin.definition + ' <br>'
                data += ' <br>'
        if data == '':
            data = word + " isn't in the dictionary"
    else:
        data = ''
    minitype = 'application/json'
    return HttpResponse(data)

@login_required
@csrf_exempt
def add_word(request, word):
    # print('sssss')
    if request.is_ajax():
        word = word.lower()
        word_object = None
        words = Word.objects.filter(word__contains=word)
        for i in range(4):
            if i == 0:
                words = Word.objects.filter(word=word)
            else:
                words = Word.objects.filter(word=word[:-i])
            if len(words) != 0:
                break
        for word in words:
            vocab_word = VocabularyWord()
            vocab_word.word = word
            vocab_word.user = request.user
            vocab_word.language = word.language
            vocab_word.save()
    # print('ddddd')
    return HttpResponse('done')