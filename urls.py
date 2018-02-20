from django.conf.urls import url
from .views import SelectPersonne, saverepetntp2, saventp2, some_pdf
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', SelectPersonne, name='SelectPersonne'),
#    url(r'^save/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/(?P<Vid>[-\w]+)/(?P<Aid>[-\w]+)/$', savereponses, name='savereponses'),
    url(r'^saverepetntp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/$', saverepetntp2, name='saverepetntp2'),
    url(r'^saventp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<Vid>[-\w]+)/(?P<Aid>[-\w]+)/$', saventp2, name='saventp2'),
#    url(r'^saverepetntp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/$', saverepetntp2, name='saverepetntp2'),
#    url(r'^saventp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/(?P<province>[-\w]+)/(?P<Vid>[-\w]+)/(?P<Aid>[-\w]+)/$', saventp2, name='saventp2'),
    url(r'^login/', auth_views.login, name='login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^pdf/(?P<pk>[-\w]+)/$', some_pdf, name='do_some_pdf'),
]
