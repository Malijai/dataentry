# -*- coding: utf-8 -*-
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User
from .models import Questionnaire, Question, Resultat, Personne, Province, Verdict, Audience
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url=settings.LOGIN_URI)
def listequestions(request):
    #affiche toutes les questions
    question_list = Question.objects.all()
    enfant_list = Question.objects.filter(parent__gt = 1)

    enfants = []
    for enfant in Question.objects.filter(parent__gt = 1):
        enfants.append(enfant.parent_id)

    parent_list=Question.objects.filter(pk__in=enfants)

    riens = Question.objects.filter(parent = 1)

    orphelins = [x for x in riens if x not in enfants and x not in parent_list]

    return render(request, 'list.html',
                  {'orphelins' : orphelins,
                   'questions': question_list,
                   'enfants': enfant_list,
                   'parents': parent_list,})


@login_required(login_url=settings.LOGIN_URI)
def savereponses(request, qid, pid, province, verdict, audience):
    #affiche le formulaire pour 1 questionnaire (qid) et 1 personne(pid) et une province (province)

    questionstoutes = Question.objects.filter(questionnaire__id=qid)
    enfants = Question.objects.filter(question__parent__id__gt=1, questionnaire=qid)
    ascendancesM = {rquestion.id for rquestion in Question.objects.filter(pk__in=enfants)}
    ascendancesF = set()  #liste sans doublons
    for rquestion in questionstoutes:
        for fille in Question.objects.filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)

    if request.method == 'POST':
        personne = Personne.objects.get(pk=pid)
        for question in questionstoutes:
            assistant = request.user
            quest = Question.objects.get(pk=question.id)
            reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                Resultat.objects.update_or_create(
                     personne=personne, question=quest, verdict_id=vvverdict, audience_id=vvaudience, assistant=assistant,
                    # update these fields, or create a new object with these values
                    defaults={
                        'reponsetexte': reponseaquestion,
                        'province_id': vvprovince,
                    }
                )
        return render(request, 'save.html',
                       {
                           'qid': qid,
                           'pid': pid,
                           'province': province,
                           'verdict': verdict,
                           'audience': audience,
                           'questions': questionstoutes,
                           'ascendancesM': ascendancesM,
                           'ascendancesF': ascendancesF,
                       }
                       )
        #    url(r'^(?P<questionnaire>[0-9]+)/save/$', views.savereponses, name='savereponses'),
    else:
        return render(request,'save.html',
                    {
                        'qid': qid,
                        'pid': pid,
                        'province': province,
                        'verdict': verdict,
                        'audience': audience,
                        'questions': questionstoutes,
                        'ascendancesM': ascendancesM,
                        'ascendancesF': ascendancesF,
                        }
                    )


@login_required(login_url=settings.LOGIN_URI)
def SelectPersonne(request):
    if request.method == 'POST':

        if request.POST.get('verdictid') == '':
            verdictid=100
        else:
            verdictid = request.POST.get('verdictid')

        if request.POST.get('audienceid') == '':
            audienceid = 100
        else:
            audienceid = request.POST.get('audienceid')

        questionnaireid = request.POST.get('questionnaireid1')
        if request.POST.get('questionnaireid1') == '' and request.POST.get('questionnaireid2') != '':
            questionnaireid = request.POST.get('questionnaireid2')
        if request.POST.get('questionnaireid2') == '' and request.POST.get('questionnaireid3') != '':
            questionnaireid = request.POST.get('questionnaireid3')
        return redirect(savereponses,
                            {
                            'qid': questionnaireid,
                            'pid': request.POST.get('personneid'),
                            'province': request.POST.get('provinceid'),
                            'verdict': verdictid,
                            'audience': audienceid
                            }
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
                'audiences': Audience.objects.all()
            }
        )


@login_required(login_url=settings.LOGIN_URI)
def savereponsesdebug(request, qid, pid):
    #affiche le formulaire pour 1 questionnaire (qid) et 1 personne(pid) et une province (province)

    enfants = Question.objects.filter(question__parent__gt=1, questionnaire=qid)
    parent_list = Question.objects.filter(pk__in=enfants)

    questionstoutes =  Question.objects.filter(questionnaire__id=qid)
    ascendancesM = {}
    meresDeF = {}
    ascendancesF  = {}
    for rquestion in parent_list:
       ascendancesM[rquestion.id]='M'  # question_id = id de la fille, la mère = parent_cond

    for rquestion in questionstoutes:
       for fille in Question.objects.filter(parent__id=rquestion.id):
            # va chercher si a des filles (question_ fille)
            meresDeF[fille.id] = rquestion.id
            ascendancesF[fille.id]='F'

    return render(
        request,
        'save42.html',
        {
            'qid': qid,
            'questions': questionstoutes,
            'pid': pid,
            'ascendancesM': ascendancesM,
            'meresDeF':meresDeF,
            'ascendancesF': ascendancesF,
            }
        )
