from django.conf.urls import url

from . import views

app_name = 'vocabulary'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^delete/(?P<v_word_id>[0-9]+)/(?P<word_id>[0-9]+)/$', views.delete, name='delete'),
]