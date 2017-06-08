from django.conf.urls import url

from . import views

app_name = 'library'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^list/(?P<list_name>[A-Za-z]+)/$', views.list_index, name='list'),
    url(r'^author/(?P<author_id>[0-9]+)/$', views.author, name='author'),
    url(r'^add/$', views.add_book, name='add_book'),
    url(r'^edit/(?P<book_id>[0-9]+)/$', views.edit_book, name='edit'),
    url(r'^delete/(?P<book_id>[0-9]+)/$', views.edit_book, name='delete'),
    url(r'^list_edit/(?P<list_name>[A-Za-z]+)/(?P<book_id>[0-9]+)/$', views.lists, name='list'),
    url(r'^private/$', views.private_index, name='private'),
]