from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.sign_in, name='sign in'),
    url(r'^signup/$', views.sign_up, name='sign up'),
    url(r'^logout/$', views.log_out, name='log out'),
    url(r'^(?P<username>[a-z]+)/$', views.detail, name='detail')
]