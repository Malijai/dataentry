from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .views import SelectPersonne

urlpatterns = [
#    url(r'^$', BlogIndex.as_view(), name='blogindex'),
    url(r'^$', SelectPersonne, name='SelectPersonne'),
    url(r'^list.html', login_required(views.listequestions), name='listequestions'),
    url(r'^save/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/(?P<verdict>[-\w]+)/(?P<audience>[-\w]+)/$', views.savereponses, name='savereponses'),
#    url(r'^(?P<pk>[-\w]+)/$', views.listequestions, name='listequestions'),
]


