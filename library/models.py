from django.db import models
from datetime import datetime
from user_manager.models import Language
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    publisher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    cover = models.ImageField(null=True, blank=True, upload_to="covers", default='covers/generic-book-cover.jpg')
    content = models.FileField(upload_to="books")
    annotation = models.TextField(default='Annotation is absent')
    private = models.BooleanField(default=False)

    def __str__(self):
        return '"%s" by %s' % (self.title, self.author)

    # def load(self):
    #     f = open(self.content., 'r')
    #     try:
    #         return f.read()
    #     except IOError:
    #         return ''


class Reaction(models.Model):
    reaction = models.BooleanField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'book'),)

    def __str__(self):
        if self.reaction:
            return '{user} likes {book}'.format(user=self.user, book=self.book)
        else:
            return '{user} dislikes {book}'.format(user=self.user, book=self.book)


class List(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ListEntry(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    time = models.DateTimeField('date added', auto_now_add=True)

    def __str__(self):
        return '{book} is in {user}\'s {list} list'.format(book=self.book, user=self.list.user, list=self.list)


class Comment(models.Model):
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #comment = models.ForeignKey('self')

    def __str__(self):
        return '{user}: {content}'.format(user=self.user, content=self.content)
