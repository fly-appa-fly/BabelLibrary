from django.conf.urls import url

from . import views

app_name = 'library'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^list/(?P<list_id>[0-9]+)/$', views.list_index, name='list'),
    url(r'^author/(?P<author_id>[0-9]+)/$', views.author, name='author'),
]