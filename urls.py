from django.conf.urls import url
from .views import SelectPersonne, saverepetntp2, saventp2, some_pdf, ffait_csv, decrypt, some_texte
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', SelectPersonne, name='SelectPersonne'),
    url(r'^saverepetntp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/$', saverepetntp2, name='saverepetntp2'),
    url(r'^saventp2/(?P<qid>[-\w]+)/(?P<pid>[-\w]+)/$', saventp2, name='saventp2'),
    url(r'^decrypt/(?P<pid>[-\w]+)', decrypt, name='decrypt'),
    url(r'^login/', auth_views.login, name='login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^pdf/(?P<pk>[-\w]+)/$', some_pdf, name='do_some_pdf'),
    url(r'^txt/(?P<pid>[-\w]+)', some_texte, name='do_some_texte'),
    url(r'^csv/$', ffait_csv, name='do_csv'),

]
