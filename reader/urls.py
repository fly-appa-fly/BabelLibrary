from django.conf.urls import url

from . import views

app_name = 'reader'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.open_book, name='open'),
    url(r'^word/(?P<word>[A-Za-z]+)/$', views.get_word, name='word'),
    url(r'^add_word/(?P<word>[A-Za-z]+)/$', views.add_word, name='word'),
]