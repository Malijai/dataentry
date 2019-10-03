from django.urls import path
from .views import select_personne, saverepetntp2, saventp2, questions_pdf, ffait_csv, decrypt, verifie_csv, \
    creerdossierntp2, fdetemps, bilan_par_province, fait_entete_ntp2_spss, fait_entete_ntp2_stata, prepare_csv
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', select_personne, name='SelectPersonne'),
    path('saverepetntp2/<int:qid>/<int:pid>/', saverepetntp2, name='saverepetntp2'),
    path('saventp2/<int:qid>/<int:pid>/', saventp2, name='saventp2'),
    path('decrypt/<int:pid>', decrypt, name='decrypt'),
    path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('pdf/<int:pk>/', questions_pdf, name='do_questions_pdf'),
    path('txt/<int:pid>', verifie_csv, name='verifie_csv'),
    path('new/', creerdossierntp2, name='creerdossierntp2'),
    path('fdt/', fdetemps, name='do_fdt'),
    path('bilan/', bilan_par_province, name='do_bilan'),
    path('csv/<int:province>/<int:questionnaire>/', prepare_csv, name='prepare_csv'),
    path('csv/<int:province>/<int:questionnaire>/<int:iteration>/<int:seuil>/', ffait_csv, name='do_csv'),
    path('entetespss/<int:questionnaire>/<int:province>/', fait_entete_ntp2_spss, name='fait_entete_ntp2_spss'),
    path('entetestata/<int:questionnaire>/<int:province>/', fait_entete_ntp2_stata, name='fait_entete_ntp2_stata'),
]
