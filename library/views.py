from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *


def index(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        results = Book.objects.filter(qset).distinct()

    else:
        results = Book.objects.order_by('-pub_date')

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 10)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books
    }
    return render(request, 'library/index.html', context)


def list_index(request, list_id):
    return HttpResponse("You're looking at list %s" % list_id)


def author(request, author_id):
    return HttpResponse("You're looking at author %s" % author_id)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book,
    }
    return render(request, 'library/detail.html', context)

