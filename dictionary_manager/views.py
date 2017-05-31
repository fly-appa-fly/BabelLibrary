from urllib.request import urlopen
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from xml.dom import minidom
from .models import *
from user_manager.models import Language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render, get_object_or_404

def get_all_text(node, word):
    definitions = Definitions()
    c = None
    if node.nodeType == node.TEXT_NODE:
        return node.data
    else:

        for child_node in node.childNodes:
            if child_node.nodeType != child_node.TEXT_NODE:
                if child_node.tagName == 'k':
                    word.word = child_node.firstChild.data.lower()
                    print(word)
                    print(word.language)
                    c = None
                elif child_node.tagName == 'c':
                    c = child_node.firstChild.firstChild.data
                elif child_node.tagName == 'b':
                    definitions = None
                    c = None
            else:
                if get_all_text(child_node, word) != '\n':
                    if definitions is None:
                        definitions = Definitions()

                    if c is not None:
                        definitions.additional_information = c + get_all_text(child_node, word)
                        definitions.save()
                    else:
                        text = get_all_text(child_node, word).split('\n')
                        definitions.type = text[1]
                        definitions.save()
                        for string in text[2:]:
                            if string != '':
                                defin = Definition()
                                defin.definition = string
                                defin.save()
                                definitions.definitions.add(defin)
                    word.definitions.add(definitions)


def load(request):
    doc = minidom.parse(urlopen('http://127.0.0.1:8000/static/oxford.xdxf'))
    words = doc.getElementsByTagName('ar')
    print(len(words))

    for w in words:
        word = Word()
        word.word = ''
        word.language = Language.objects.get(id=1)
        word.save()
        print(get_all_text(w, word))
        word.save()
        print(word)


def index(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(word__icontains=query)
        )
        results = Word.objects.filter(qset).distinct()

    else:
        results = Word.objects.order_by('word')

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 100)

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    context = {
        'words': words
    }
    return render(request, 'dictionary_manager/index.html', context)


def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    context = {
        'word': word,
    }
    return render(request, 'dictionary_manager/detail.html', context)

def get_word(request, word):
    return HttpResponse('ssssss')