from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import *


@login_required
def index(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(word__icontains=query),
            Q(user=request.user)
        )
        results = Word.objects.filter(qset).distinct()

    else:
        results = VocabularyWord.objects.order_by('word')

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
