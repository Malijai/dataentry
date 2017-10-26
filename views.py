# -*- coding: utf-8 -*-
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User
from .models import Questionnaire, Question, Resultat, Personne, Province, Verdict, Audience, AFSF
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

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
def SelectPersonne(request):
    if request.method == 'POST':
        if 'Choisir1' in request.POST:
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
                return redirect(savereponses,
                                    request.POST.get('questionnaireid'),
                                    request.POST.get('personneid'),
                                    request.POST.get('provinceid'),
                                    request.POST.get('verdictid1'),
                                    request.POST.get('audienceid1')
                        )
        elif 'Choisir2' in request.POST:
            if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '' or request.POST.get('provinceid') == '' or request.POST.get('verdictid2') == '':
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
                return redirect(savereponses,
                            request.POST.get('questionnaireid'),
                            request.POST.get('personneid'),
                            request.POST.get('provinceid'),
                            request.POST.get('verdictid2'),
                            request.POST.get('audienceid2')
                            )

        elif 'Choisir3' in request.POST:
            if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '' or request.POST.get(
                    'provinceid') == '' or request.POST.get('verdictid3') == '' or request.POST.get('audience3') == '':
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
                return redirect(savereponses,
                        request.POST.get('questionnaireid'),
                        request.POST.get('personneid'),
                        request.POST.get('provinceid'),
                        request.POST.get('verdictid3'),
                        request.POST.get('audienceid3')
                        )

        elif 'Choisir4' in request.POST:
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
                return redirect(saveafsf,
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
def savereponses(request, qid, pid, province, Vid, Aid):
    questionstoutes = Question.objects.filter(questionnaire__id=qid)
    enfants = Question.objects.filter(question__parent__id__gt=0, questionnaire=qid)
    ascendancesM = {rquestion.id for rquestion in Question.objects.filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in Question.objects.filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)

    if request.method == 'POST':
        for question in questionstoutes:
            assistant = request.user
            quest = Question.objects.get(pk=question.id)
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
        return render(request, 'save.html',
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
        return render(request, 'save.html',
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
def saveafsf(request, qid, pid, province):
    questionstoutes = Question.objects.filter(questionnaire__id=qid)
    enfants = Question.objects.filter(question__parent__id__gt=0, questionnaire=qid)
    ascendancesM = {rquestion.id for rquestion in Question.objects.filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in Question.objects.filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
    fiches = AFSF.objects.filter(personne__id=pid, assistant__id=request.user.id)
    ordre = AFSF.objects.filter(personne__id=pid, assistant__id=request.user.id).count()

    if request.method == 'POST':
        for question in questionstoutes:
            assistant = request.user
            quest = Question.objects.get(pk=question.id)
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
                champ = quest.varname
                AFSF.objects.update_or_create(
                     personne_id=pid, assistant=assistant, AFSF_order=ordre,
                    # update these fields, or create a new object with these values
                    defaults={
                        champ : reponseaquestion,
                    }
                )
        now = datetime.datetime.now().strftime('%H:%M:%S')
        if 'add' in request.POST:
            ordre = AFSF.objects.filter(personne__id=pid, assistant__id=request.user.id).count()
            ordre = ordre + 1
            AFSF.objects.create(personne_id=pid, assistant=assistant, AFSF_order=ordre,
                # update these fields, or create a new object with these values
            )
            messages.add_message(request, messages.WARNING, 'Data saved and file added at ' + now)
        else:
             messages.add_message(request, messages.WARNING, 'Data saved at ' + 'time' + now)

        return render(request, 'saveafsf.html',
                      {
                          'qid': qid,
                          'pid': pid,
                          'province': province,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF,
                          'fiches': fiches
                      }
                      )

    else:
         return render(request, 'saveafsf.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'province': province,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF,
                      'fiches': fiches
                  }
                  )