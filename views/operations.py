# -*- coding: utf-8 -*-
from django.shortcuts import  render, redirect
from dataentry.models import Questionnaire, Personne
from dataentry.models import Resultatrepetntp2, Questionntp2, Resultatntp2
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import datetime
#import logging
from dataentry.encrypter import Encrypter


@login_required(login_url=settings.LOGIN_URI)
def SelectPersonne(request):
    #Pour selectionner province, personne, questionnaire
    province = request.user.profile.province
    if request.method == 'POST':
        if 'Choisir1' in request.POST:
            #pour le NON repetitif
            if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '': #or request.POST.get('provinceid') == '':
                messages.add_message(request, messages.ERROR, 'You have forgotten to chose at least one field')
                if province == 10:
                    return render(
                                request,
                                'choix.html',
                                {
                                    'personnes': Personne.objects.objects.all(),
                                    'questionnaires': Questionnaire.objects.all(),
                                }
                            )
                else:
                    return render(
                                request,
                                'choix.html',
                                {
                                    'personnes': Personne.objects.filter(province__id=province),
                                    'questionnaires': Questionnaire.objects.all(),
                                }
                            )
            else:
                return redirect(
                                saventp2,
                                request.POST.get('questionnaireid'),
                                request.POST.get('personneid'),
                            )

        elif 'Choisir4' in request.POST:
            # pour le REPETITIF
            if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '': # or request.POST.get('provinceid') == '' :
                messages.add_message(request, messages.ERROR, 'You have forgotten to chose at least one field')
                if province == 10:
                    return render(
                                request,
                                'choix.html',
                                {
                                    'personnes': Personne.objects.objects.all(),
                                    'questionnaires': Questionnaire.objects.all(),
                                }
                            )
                else:
                    return render(
                                request,
                                'choix.html',
                                {
                                    'personnes': Personne.objects.filter(province__id=province),
                                    'questionnaires': Questionnaire.objects.all(),
                                }
                            )
            else:
                return redirect(saverepetntp2,
                                request.POST.get('questionnaireid'),
                                request.POST.get('personneid'),
                                #request.POST.get('provinceid'),
                                )

    else:
        if province == 10:
            return render(
                request,
                'choix.html',
                {
                    'personnes': Personne.objects.objects.all(),
                    'questionnaires': Questionnaire.objects.all(),
                }
            )
        else:
            return render(
                        request,
                        'choix.html',
                        {
                            #'personnes': Personne.objects.all(),
                            'personnes': Personne.objects.filter(province__id=province),
                            'questionnaires': Questionnaire.objects.all(),
                            'message':'welcome'
                        }
                    )


@login_required(login_url=settings.LOGIN_URI)
def saventp2(request, qid, pid):#(request, qid, pid, province):
    #genere le questionnaire demande NON repetitif
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code
    questionnaire = Questionnaire.objects.get(id=qid).nom_en

    if request.method == 'POST':
        for question in questionstoutes:
            assistant = request.user
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'DATEH':
                an = request.POST.get('q' + str(question.id) + '_year')
                if an != "":
                    mois = request.POST.get('q' + str(question.id) + '_month')
                    jour = request.POST.get('q' + str(question.id) + '_day')
                    reponseaquestion = str(an) + '-' + str(mois) + '-' + str(jour)
                else:
                    reponseaquestion = ''
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    #reponseaquestion = encode_donnee(reponseaquestion)
                    reponseaquestion = 'Encoded'

                Resultatntp2.objects.update_or_create(
                             personne_id=pid, question_id=question.id, assistant=assistant,
                            # update these fields, or create a new object with these values
                            defaults={
                                'reponsetexte': reponseaquestion,
                            }
                        )
        now = datetime.datetime.now().strftime('%H:%M:%S')
        messages.add_message(request, messages.WARNING, 'Data saved at ' + now)
        return render(request, 'saventp2.html',
                      {
                          'qid': qid,
                          'pid': pid,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF,
                          'code' : nomcode,
                          'questionnaire' : questionnaire
                      }
                      )
    else:
        return render(request, 'saventp2.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF,
                      'code': nomcode,
                      'questionnaire': questionnaire
                  }
                  )


@login_required(login_url=settings.LOGIN_URI)
def saverepetntp2(request, qid, pid):#(request, qid, pid, province):
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code

    if request.method == 'POST':
 #       assistant = request.user
        actions = request.POST.keys()
        for action in actions:
            if action.startswith('remove_'):
                x = action[len('remove_'):]
                Resultatrepetntp2.objects.filter(personne__id=pid, assistant__id=request.user.id, questionnaire__id=qid, fiche=x ).delete()
                messages.add_message(request, messages.ERROR, 'Card # ' + str(x) + ' removed')
                continue
            elif action.startswith('current_') or action.startswith('add_'):
                if action.startswith('current_'):
                    x = action[len('current_'):]
                else:
                    x = action[len('add_'):]
                    enregistrement = Resultatrepetntp2.objects.filter(
                                        personne__id=pid,
                                        assistant__id=request.user.id,
                                        questionnaire__id=qid).order_by('-fiche').first()
                    ordre = enregistrement.fiche + 1
                    Resultatrepetntp2.objects.create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                question_id=1,
                                fiche=ordre,
                                reponsetexte= 10000
                            )
                    messages.add_message(request, messages.WARNING, '1 File added ')

                for question in questionstoutes:
                    if question.typequestion_id == 5 or question.typequestion_id == 60:
                        an = request.POST.get('q' + str(question.id) + 'Z_Z' + str(x) + '_year')
                        if an != "":
                            mois = request.POST.get('q' + str(question.id) + 'Z_Z' + str(x) + '_month' )
                            jour = request.POST.get('q' + str(question.id)+ 'Z_Z' + str(x) + '_day' )
                            reponseaquestion = str(an) + '-' + str(mois) + '-' + str(jour)
                        else:
                            reponseaquestion = ''
                    else:
                        reponseaquestion = request.POST.get('q' + str(question.id) + 'Z_Z' + str(x))
                    if reponseaquestion:
                        Resultatrepetntp2.objects.update_or_create(
                                            personne_id=pid,
                                            assistant_id=request.user.id,
                                            questionnaire_id=qid,
                                            question_id=question.id,
                                            fiche=x,
                                            # update these fields, or create a new object with these values
                                            defaults={'reponsetexte': reponseaquestion}
                                        )
                now = datetime.datetime.now().strftime('%H:%M:%S')
                messages.add_message(request, messages.WARNING, 'Data saved at ' + now)

        compte, fiches = fait_pagination(pid, qid, request)
        return render(
                    request,
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
                    }
                )
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
        return render(request, 'saverepetntp2.html',
                      {
                          'qid': qid,
                          'pid': pid,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF,
                          'fiches': fiches,
                          'compte': compte,
                          'code': nomcode,
                      }
                      )


def fait_pagination(pid, qid, request):
    fiche_list = Resultatrepetntp2.objects.filter(personne__id=pid, assistant__id=request.user.id,
                                                  questionnaire__id=qid)
    donnees = fiche_list.values_list('fiche', flat=True).distinct()
    compte = donnees.count()
    paginator = Paginator(donnees, 3)  # Show 5 fiches par page
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
    enfants = questionstoutes.select_related('typequestion', 'parent').filter(questionntp2__parent__id__gt=0)
    ascendancesM = {rquestion.id for rquestion in questionstoutes.select_related('typequestion').filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in questionstoutes.select_related('typequestion').filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
    return ascendancesF, ascendancesM, questionstoutes


def encode_donnee(message):
    PK_path = settings.PUBLIC_KEY_PATH
    PK_name = settings.PUBLIC_KEY
    e = Encrypter()
    #public_key = e.read_key(PK_path + 'Manitoba_public.pem')
    public_key = e.read_key(PK_path + PK_name)
    return e.encrypt(message,public_key)

