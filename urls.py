from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .views import SelectPersonne, saverepetntp2, saventp2

urlpatterns = [
    url(r'^$', SelectPersonne, name='SelectPersonne'),
#    url(r'^save/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/(?P<Vid>[-\w]+)/(?P<Aid>[-\w]+)/$', savereponses, name='savereponses'),
    url(r'^saverepetntp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/$', saverepetntp2, name='saverepetntp2'),
    url(r'^saventp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/(?P<Vid>[-\w]+)/(?P<Aid>[-\w]+)/$', saventp2, name='saventp2')
]
