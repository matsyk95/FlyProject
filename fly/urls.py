from django.conf.urls import url
from django.urls import path
from . import views




app_name = 'fly'
urlpatterns = [
    #/fly
    url(r'^$', views.index, name='index'),
    url(r'^(?P<fly_id>[0-9]+)/$', views.search, name='results'),
    url(r'^register$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^detail/$', views.detail, name='detail'),
]
