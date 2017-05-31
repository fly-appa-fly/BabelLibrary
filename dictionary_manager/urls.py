from django.conf.urls import url

from . import views

app_name = 'dict'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^word/(?P<word_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<word>[A-Za-z]+)/$', views.get_word, name='word')
]