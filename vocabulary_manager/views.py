from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import *


@login_required
def index(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(word__icontains=query),
        )
        results = VocabularyWord.objects.filter(qset).distinct().filter(user=request.user)

    else:
        results = VocabularyWord.objects.filter(user=request.user).order_by('word')

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
    return render(request, 'vocabulary_manager/index.html', context)


@login_required
def delete(request, v_word_id, word_id):
    v_word = get_object_or_404(VocabularyWord, pk=v_word_id)

    if request.user == v_word.user:
        v_word.delete()
        return redirect('/dict/word' + word_id)
    return redirect('/')