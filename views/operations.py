# -*- coding: utf-8 -*-
import datetime
# import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from dataentry.encrypter import Encrypter
from dataentry.dataentry_constants import LISTE_PROVINCE
from dataentry.models import Personne, Province
from accueil.models import Profile, User
from dataentry.models import Questionnaire, Resultatrepetntp2, Questionntp2, Resultatntp2


@login_required(login_url=settings.LOGIN_URI)
def select_personne(request):
    # Pour selectionner personne (en fonction de la province), questionnaire
    province = request.user.profile.province
    if province == 10:
        personnes = Personne.objects.all()
    else:
        personnes = Personne.objects.filter(province__id=province).filter(~Q(completed=1))

    if request.method == 'POST':
        if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '':
            messages.add_message(request, messages.ERROR, 'You have forgotten to chose at least one field')
            return render(
                request,
                'choix.html',
                {
                'personnes': personnes,
                'questionnaires': Questionnaire.objects.all(),
                }
                )

        if 'Choisir1' in request.POST:
            #   pour le NON repetitif
            return redirect(
                            saventp2,
                            request.POST.get('questionnaireid'),
                            request.POST.get('personneid'),
                            )

        elif 'Repetitif' in request.POST:
            # pour le REPETITIF
            return redirect(saverepetntp2,
                                request.POST.get('questionnaireid'),
                                request.POST.get('personneid'),
                                )
        elif 'Creer' in request.POST:
            return redirect(creerdossierntp2)
        elif 'Fermer' in request.POST:
            # pour fermer un dossier
            pid = request.POST.get('personneid')
            personne2 = Personne.objects.get(pk=pid)
            if Personne.objects.filter(pk=pid, assistant=request.user).exists():
                personne = Personne.objects.get(pk=pid, assistant=request.user)
                personne.completed = 1
                personne.save()
                messages.add_message(request, messages.WARNING, personne.code + ' has been closed')
            else:
                messages.add_message(request, messages.ERROR, personne2.code + ' You are not allowed to close this file as you didn''t create it')
            return render(
                    request,
                    'choix.html',
                    {
                        'personnes': personnes,
                        'questionnaires': Questionnaire.objects.all(),
                        'message': 'welcome'
                    }
                )
        elif 'Verifier' in request.POST:
            # pour fermer un dossier
            pid = request.POST.get('personneid')
            return redirect('verifie_csv', pid=pid)
        elif 'Exporterdata' in request.POST:
            questionnaire = request.POST.get('questionnaireid')
            province= request.POST.get('provinceid')
            return redirect('prepare_csv', province=province, questionnaire=questionnaire)
        elif 'fait_entete_ntp2_spss' in request.POST:
            questionnaire = request.POST.get('questionnaireid')
            province= request.POST.get('provinceid')
            return redirect('fait_entete_ntp2_spss', province=province, questionnaire=questionnaire)
        elif 'fait_entete_ntp2_stata' in request.POST:
            questionnaire = request.POST.get('questionnaireid')
            province= request.POST.get('provinceid')
            return redirect('fait_entete_ntp2_stata', province=province, questionnaire=questionnaire)
    else:
        return render(
                    request,
                    'choix.html',
                    {
                        'personnes': personnes,
                        'questionnaires': Questionnaire.objects.all(),
                        'provinces2': Province.objects.all(),
                        'message': 'welcome'
                    }
                )


@login_required(login_url=settings.LOGIN_URI)
def creerdossierntp2(request):
    qid = 500
    questionstoutes = Questionntp2.objects.filter(questionnaire__id=qid)
    if request.method == 'POST':
        reponses = {}
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE':
                an = request.POST.get('q{}_year'.format(question.id))
                if an != "":
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                else:
                    reponseaquestion = ''
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    reponseaquestion = encode_donnee(reponseaquestion)
                reponses[question.varname] = reponseaquestion
        prov = LISTE_PROVINCE[request.user.profile.province]
        pref = request.user.profile.province * 10000
        dernier = Personne.objects.all().order_by('-id').first()
        reponses['personne_code'] = "{}_{}".format(prov, pref + dernier.id + 1,)
        Personne.objects.create(
                                code=reponses['personne_code'],
                                hospcode=reponses['hospcode'],
                                selecthosp=reponses['SelectHosp'],
                                province_id=request.user.profile.province,
                                date_indexh=reponses['RDIH'],
                                assistant_id=request.user.id
                                )
        textefin=  "{}  has been created".format(reponses['personne_code'])
        messages.add_message(request, messages.ERROR, textefin)
        return redirect(select_personne)
    else:
        return render(
                    request,
                    'createntp2.html',
                    {'questions': questionstoutes}
                )


@login_required(login_url=settings.LOGIN_URI)
def saventp2(request, qid, pid):
    #   genere le questionnaire demande NON repetitif
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code
    hospcode = Personne.objects.get(id=pid).hospcode
    questionnaire = Questionnaire.objects.get(id=qid).nom_en

    if request.method == 'POST':
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE' or \
                            question.typequestion.nom == 'DATEH':
                an = request.POST.get('q{}_year'.format(question.id))
                if an != "":
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                else:
                    reponseaquestion = ''
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    reponseaquestion = encode_donnee(reponseaquestion)
                    personne = Personne.objects.get(pk=pid)
                    personne.__dict__[question.varname] = reponseaquestion
                    personne.assistant = request.user
                    personne.save()
                else:
                    if not Resultatntp2.objects.filter(personne_id=pid, question=question, assistant=request.user,
                                                       reponsetexte=reponseaquestion).exists():
                        Resultatntp2.objects.update_or_create(personne_id=pid, question=question, assistant=request.user,
                                # update these fields, or create a new object with these values
                                defaults={
                                    'reponsetexte': reponseaquestion,
                                }
                            )
        now = datetime.datetime.now().strftime('%H:%M:%S')
        messages.add_message(request, messages.WARNING, 'Data saved at ' + now)

    return render(request,
                  'saventp2.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF,
                      'code': nomcode,
                      'hospcode' : hospcode,
                      'questionnaire': questionnaire,
                  }
                )


@login_required(login_url=settings.LOGIN_URI)
def saverepetntp2(request, qid, pid):
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code
    hospcode = Personne.objects.get(id=pid).hospcode
    questionnaire = Questionnaire.objects.get(id=qid).nom_en

    if request.method == 'POST':
        actions = request.POST.keys()
        for action in actions:
            if action.startswith('remove_'):
                x = action[len('remove_'):]
                Resultatrepetntp2.objects.filter(personne__id=pid, assistant=request.user, questionnaire__id=qid,
                                                 fiche=x).delete()
                messages.add_message(request, messages.ERROR, 'Card # ' + str(x) + ' removed')
                continue
            elif action.startswith('current_') or action.startswith('add_'):
                if action.startswith('current_'):
                    x = action[len('current_'):]
                else:
                    x = action[len('add_'):]
                    enregistrement = Resultatrepetntp2.objects.filter(
                                        personne__id=pid,
                                        assistant=request.user,
                                        questionnaire__id=qid).order_by('-fiche').first()
                    ordre = enregistrement.fiche + 1
                    Resultatrepetntp2.objects.create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                question_id=1,
                                fiche=ordre,
                                reponsetexte=10000
                            )
                    messages.add_message(request, messages.WARNING, '1 Card added ')

                for question in questionstoutes:
                    if question.typequestion_id == 5 or question.typequestion_id == 60:
                        an = request.POST.get('q{}Z_Z{}_year'.format(question.id, x))
                        if an != "":
                            mois = request.POST.get('q{}Z_Z{}_month'.format(question.id, x))
                            jour = request.POST.get('q{}Z_Z{}_day'.format(question.id, x))
                            reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                        else:
                            reponseaquestion = ''
                    else:
                        reponseaquestion = request.POST.get('q{}Z_Z{}'.format(question.id, x))
                    if reponseaquestion:
                        if not Resultatrepetntp2.objects.filter(personne_id=pid,
                                                                assistant_id=request.user.id,
                                                                questionnaire_id=qid,
                                                                question_id=question.id,
                                                                fiche=x,
                                                                reponsetexte=reponseaquestion).exists():
                            Resultatrepetntp2.objects.update_or_create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                question_id=question.id,
                                fiche=x,
                                # update these fields, or create a new object with these values
                                defaults={
                                    'reponsetexte': reponseaquestion,
                                }
                            )
                now = datetime.datetime.now().strftime('%H:%M:%S')
                messages.add_message(request, messages.WARNING, 'Data saved at ' + now)

    else:
        if Resultatrepetntp2.objects.filter(personne_id=pid, assistant_id=request.user.id, questionnaire_id=qid).count() == 0:
            Resultatrepetntp2.objects.create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                question_id=1,
                                fiche=1,
                                reponsetexte=10000
                            )

    compte, fiches = fait_pagination(pid, qid, request)
    return render(request,
                      'saverepetntp2.html',
                      {
                          'qid': qid,
                          'pid': pid,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF,
                          'fiches': fiches,
                          'compte': compte,
                          'code': nomcode,
                          'hospcode': hospcode,
                          'questionnaire': questionnaire,
                      }
                  )


def fait_pagination(pid, qid, request):
    donnees = Resultatrepetntp2.objects.order_by('fiche').filter(
                        personne__id=pid, assistant__id=request.user.id, questionnaire__id=qid
                        ).values_list('fiche', flat=True).distinct()
    #donnees = fiche_list.values_list('fiche', flat=True).distinct()
    compte = donnees.count()
    paginator = Paginator(donnees, 3)  # Show 3 fiches par page
    page = request.GET.get('page')
    try:
        fiches = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fiches = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fiches = paginator.page(paginator.num_pages)
    return compte, fiches


def genere_questions(qid):
    questionstoutes = Questionntp2.objects.filter(questionnaire__id=qid)
    enfants = questionstoutes.select_related('typequestion', 'parent').filter(questionntp2__parent__id__gt=1)
    ascendancesM = {rquestion.id for rquestion in questionstoutes.select_related('typequestion').filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in questionstoutes.select_related('typequestion').filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
    return ascendancesF, ascendancesM, questionstoutes


def encode_donnee(message):
    PK_path = settings.PUBLIC_KEY_PATH
    PK_name = settings.PUBLIC_KEY_NTP2
    e = Encrypter()
    #   public_key = e.read_key(PK_path + 'Manitoba_public.pem')
    public_key = e.read_key(PK_path + PK_name)
    return e.encrypt(message,public_key)


def bilan_par_province(request):
    nb_dossiers_par_p = Province.objects.annotate(num_dossiers=Count('personne', filter=Q(personne__completed=1)))
    nb_dossiers_par_ar = User.objects.annotate(nb_dossiers=Count('personne', filter=Q(personne__completed=1)))
    nb_repet = Resultatrepetntp2.objects.values('personne','questionnaire','assistant').order_by().filter(Q(personne__completed=1)).annotate(nb_h=Count('fiche', distinct=True))
    assistants = set([])
    questionnaires = set([])
    repet_par_ass = {}
    for nbh in nb_repet:
        assistant = nbh['assistant']
        questionnaire = nbh['questionnaire']
        if not assistant in assistants:
            assistants.add(assistant)
        if not questionnaire in questionnaires:
            questionnaires.add(questionnaire)
        pers_prec = repet_par_ass.get((assistant, questionnaire), 0)
        nb = pers_prec + nbh['nb_h']
        repet_par_ass[assistant, questionnaire] = nb

#    nb_repet2 = Questionnaire.objects.annotate(nb_h2=Count('resultatrepetntp2__fiche', distinct=True, filter=Q(id=2000) | Q(id=3000)))
#    requete = str(nb_repet.query)
# select questionnaire_id, count(distinct fiche)
# from dataentry_resultatrepetntp2
# group by questionnaire_id, assistant_id, personne_id
    return render(
        request,
        'bilan.html',
         {
            'dossiers': nb_dossiers_par_p,
            'indexh': nb_dossiers_par_ar,
            'assistants': assistants,
            'questionnaires': questionnaires,
            'repet_par_ass': repet_par_ass
             #            'requete': requete
         }
    )

@login_required(login_url=settings.LOGIN_URI)
def deletentp2(request, qid, pid):
    #   genere le questionnaire demande NON repetitif
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code
    hospcode = Personne.objects.get(id=pid).hospcode
    questionnaire = Questionnaire.objects.get(id=qid).nom_en

    if request.method == 'POST':
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE' or \
                            question.typequestion.nom == 'DATEH':
                an = request.POST.get('q{}_year'.format(question.id))
                if an != "":
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                else:
                    reponseaquestion = ''
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    reponseaquestion = encode_donnee(reponseaquestion)
                    personne = Personne.objects.get(pk=pid)
                    personne.__dict__[question.varname] = reponseaquestion
                    personne.assistant = request.user
                    personne.save()
                else:
                    if not Resultatntp2.objects.filter(personne_id=pid, question=question, assistant=request.user,
                                                       reponsetexte=reponseaquestion).exists():
                        Resultatntp2.objects.update_or_create(personne_id=pid, question=question, assistant=request.user,
                                # update these fields, or create a new object with these values
                                defaults={
                                    'reponsetexte': reponseaquestion,
                                }
                            )
        now = datetime.datetime.now().strftime('%H:%M:%S')
        messages.add_message(request, messages.WARNING, 'Data saved at ' + now)

    return render(request,
                  'saventp2.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF,
                      'code': nomcode,
                      'hospcode' : hospcode,
                      'questionnaire': questionnaire,
                  }
                )

def genere_questions_deletion(qid):
    questionstoutes = Questionntp2.objects.filter(questionnaire__id=qid)
    enfants = questionstoutes.select_related('typequestion', 'parent').filter(questionntp2__parent__id__gt=1)
    ascendancesM = {rquestion.id for rquestion in questionstoutes.select_related('typequestion').filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in questionstoutes.select_related('typequestion').filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
    return ascendancesF, ascendancesM, questionstoutes

