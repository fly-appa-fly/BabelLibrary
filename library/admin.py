from django.contrib import admin

from .models import Book, Author, Comment, List, Tag
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(List)
admin.site.register(Tag)
