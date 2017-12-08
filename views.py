# -*- coding: utf-8 -*-
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Questionnaire, Question, Resultat, Personne, Province, Verdict, Audience, Resultatrepetntp2,Questionntp2
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.apps import apps
import datetime
import logging


@login_required(login_url=settings.LOGIN_URI)
def SelectPersonne(request):
    #Pour selectionner province, personne, questionnaire
    if request.method == 'POST':
        if 'Choisir1' in request.POST:
            #pour le NON repetitif
            if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '' or request.POST.get('provinceid') == '':
                messages.add_message(request, messages.ERROR, 'You have forgotten to chose at least one field')
                return render(
                    request,
                    'choix.html',
                    {
                        'personnes': Personne.objects.all(),
                        'questionnaires': Questionnaire.objects.all(),
                        'provinces': Province.objects.all(),
                        'verdicts': Verdict.objects.all(),
                        'audiences': Audience.objects.all(),
                    }
                )
            else:
                return redirect(saventp2,
                                    request.POST.get('questionnaireid'),
                                    request.POST.get('personneid'),
                                    request.POST.get('provinceid'),
                                    request.POST.get('verdictid1'),
                                    request.POST.get('audienceid1')
                        )

        elif 'Choisir4' in request.POST:
            # pour le REPETITIF
            if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '' or request.POST.get(
                    'provinceid') == '' :
                messages.add_message(request, messages.ERROR, 'You have forgotten to chose at least one field')
                return render(
                    request,
                    'choix.html',
                    {
                        'personnes': Personne.objects.all(),
                        'questionnaires': Questionnaire.objects.all(),
                        'provinces': Province.objects.all(),
                        'verdicts': Verdict.objects.all(),
                        'audiences': Audience.objects.all()
                    }
                )
            else:
                return redirect(saverepetntp2,
                        request.POST.get('questionnaireid'),
                        request.POST.get('personneid'),
                        request.POST.get('provinceid'),
                        )

    else:
         return render(
            request,
            'choix.html',
            {
                'personnes': Personne.objects.all(),
                'questionnaires': Questionnaire.objects.all(),
                'provinces': Province.objects.all(),
                'verdicts': Verdict.objects.all(),
                'audiences': Audience.objects.all(),
                'message':'welcome'
            }
        )


@login_required(login_url=settings.LOGIN_URI)
def saventp2(request, qid, pid, province, Vid, Aid):
    #genere le questionnaire demande NON repetitif
    questionstoutes = Questionntp2.objects.filter(questionnaire__id=qid)
    enfants = Questionntp2.objects.filter(questionntp2__parent__id__gt=0, questionnaire=qid)
    ascendancesM = {rquestion.id for rquestion in Questionntp2.objects.filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in Questionntp2.objects.filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)

    if request.method == 'POST':
        for question in questionstoutes:
            assistant = request.user
            quest = Questionntp2.objects.get(pk=question.id)
            if quest.typequestion_id == 5:
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
                Resultat.objects.update_or_create(
                     personne_id=pid, question=quest, verdict_id=Vid, audience_id=Aid, assistant=assistant,
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
                          'province': province,
                          'Vid': Vid,
                          'Aid': Aid,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF
                      }
                      )

    else:
        return render(request, 'saventp2.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'province': province,
                      'Vid': Vid,
                      'Aid': Aid,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF
                  }
                  )


@login_required(login_url=settings.LOGIN_URI)
def saverepetntp2(request, qid, pid, province):
    questionstoutes = Questionntp2.objects.filter(questionnaire__id=qid)
    enfants = Questionntp2.objects.filter(questionntp2__parent__id__gt=0, questionnaire=qid)
    ascendancesM = {rquestion.id for rquestion in Questionntp2.objects.filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in Questionntp2.objects.filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
#    questiontable = {"100": "afsf", }
#    Klass = apps.get_model('dataentry', questiontable[str(qid)])


    if request.method == 'POST':
        assistant = request.user
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
                    Resultatrepetntp2.objects.update_or_create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                question_id=10000,
                                fiche=ordre,
                                # update these fields, or create a new object with these values
                                defaults={'reponsetexte': 10000}
                            )
                    messages.add_message(request, messages.WARNING, '1 File added ')

                for question in questionstoutes:
                    if question.typequestion_id == 5:
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
                        'province': province,
                        'questions': questionstoutes,
                        'ascendancesM': ascendancesM,
                        'ascendancesF': ascendancesF,
                        'fiches': fiches,
                        'compte': compte,
                    }
                )
    else:
        if Resultatrepetntp2.objects.filter(personne_id=pid, assistant_id=request.user.id, questionnaire_id=qid).count() == 0:
            Resultatrepetntp2.objects.update_or_create(
                        personne_id=pid,
                        assistant_id=request.user.id,
                        questionnaire_id=qid,
                        question_id=10000,
                        fiche=1,
                        # update these fields, or create a new object with these values
                        defaults={'reponsetexte': 10000}
                    )

        compte, fiches = fait_pagination(pid, qid, request)
        return render(request, 'saverepetntp2.html',
                      {
                          'qid': qid,
                          'pid': pid,
                          'province': province,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF,
                          'fiches': fiches,
                          'compte': compte,
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