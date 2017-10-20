from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .views import SelectPersonne, savereponses

urlpatterns = [
    url(r'^$', SelectPersonne, name='SelectPersonne'),
    url(r'^save/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/(?P<Vid>[-\w]+)/(?P<Aid>[-\w]+)/$', savereponses, name='savereponses'),
]
