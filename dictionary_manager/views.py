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


def get_text(node):
    if node.nodeType == node.TEXT_NODE:
        return node.data
    else:
        text_string = ""
        for child_node in node.childNodes:
            if child_node.nodeType != child_node.TEXT_NODE:
                text_string += get_text(child_node.firstChild)
            else:
                text_string += child_node.data
        return text_string


def get_all_text(node):
    words = None
    text = ''
    if node.nodeType == node.TEXT_NODE:
        return node.data
    else:

        for child_node in node.childNodes:
            if child_node.nodeType != child_node.TEXT_NODE:
                if child_node.tagName == 'k':
                    w = child_node.firstChild.data.lower()
                    words = Word.objects.filter(language=1, word__exact=w)
                else:
                    text += get_text(child_node.firstChild)
            else:
                text += get_text(child_node)
    if len(words) != 0:
        trans = Translation()
        trans.translation_to = Language.objects.get(pk=2)
        trans.translation = text
        print(trans.translation_to)
        print(trans.translation)
        trans.save()
        for word in words:
            word.translations.add(trans)
            word.save()
    #text = get_text(node)


def load(request):
    doc = minidom.parse(urlopen('http://127.0.0.1:8000/static/eng-ukr.xdxf'))
    words = doc.getElementsByTagName('ar')
    print(len(words))

    for w in words:
        get_all_text(w)


def index(request):
    #load(request)

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

    index_ = words.number - 1
    max_index = len(paginator.page_range)
    start_index = index_ - 3 if index_ >=3 else 0
    end_index = index_ + 4 if index_ <= max_index - 4 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'words': words,
        'page_range': page_range,
        'last': max_index
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