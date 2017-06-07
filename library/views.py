from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import BookForm


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

    index_ = books.number - 1
    max_index = len(paginator.page_range)
    start_index = index_ - 3 if index_ >= 3 else 0
    end_index = index_ + 4 if index_ <= max_index - 4 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'books': books,
        'page_range': page_range,
        'last': max_index
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


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            authors = Author.objects.filter(first_name=first_name, last_name=last_name)
            if len(authors) != 0:
                update.author = authors[0]
            else:
                auth = Author()
                auth.first_name = first_name
                auth.last_name = last_name
                auth.save()
                update.author = auth

            update.save()
            return redirect('/')
    else:
        lang_choices = [(c.id, c.eng_name) for c in Language.objects.all()]
        tag_choices = [(c.id, c.name) for c in Tag.objects.all()]
        form = BookForm()
        form.fields['tags'].choices = tag_choices
        form.fields['language'].choices = lang_choices
    return render(request, 'library/add_book.html', {'form': form})
