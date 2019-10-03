# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dataentry.models import Questionnaire, Questionntp2, Reponsentp2, Personne, Resultatntp2, \
    Resultatrepetntp2, Etablissement, Municipalite
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from dataentry.dataentry_constants import CHOIX_ONUK, LISTE_PROVINCE
from accueil.models import Projet, Profile
from django.db.models import Q, Count
from django.template import loader
import csv
import datetime


DATE = datetime.datetime.now().strftime('%Y %b %d')


# Pour l'exportation en streaming du CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value


## Sortie des donnees Individuelles un dossier a la fois
# Pour verifier les donees de base avant de clore un dossier
@login_required(login_url=settings.LOGIN_URI)
def verifie_csv(request, pid):
    # Pour exporter les données de base (les questions qui ont l'attribu qstyle=1 pour tous les cas
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    province = request.user.profile.province
    personne = Personne.objects.get(pk=pid)
    csv_data = ([])
    debut = ['Province & File code', personne.province.reponse_en, personne.code]
    csv_data.append(debut)
    questionnaires = Questionnaire.objects.filter(id__gt=1)
    for questionnaire in questionnaires:
        questions = Questionntp2.objects.filter(qstyle=1, questionnaire_id=questionnaire.id).order_by('questionno')
        ligne2 = [questionnaire.nom_en]
        csv_data.append(ligne2)
        if questionnaire.id < 2000:
            for question in questions:
                ligne = [question.varname, question.questionen]
                donnee = Resultatntp2.objects.filter(personne__id=pid, question__id=question.id, assistant__id=request.user.id,)
                if donnee:
                    reponse = fait_reponse(donnee[0].reponsetexte, question, province)
                    ligne.append(reponse)
                else:
                    ligne.append('-')
                csv_data.append(ligne)
        else:
            donnees = Resultatrepetntp2.objects.order_by().filter(personne__id=pid, assistant__id=request.user.id, questionnaire__id=questionnaire.id).values_list('fiche', flat=True).distinct()
            compte = donnees.count()
            ligne2 = [str(compte) + ' different ' + questionnaire.nom_en]
            csv_data.append(ligne2)
            fait_repetitives(csv_data, donnees, pid, province, questions, request)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer,dialect="excel-tab")
    response = StreamingHttpResponse((writer.writerow(row) for row in csv_data),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename={}.txt'.format(personne.code)
    return response


# Fait les requetes dans la BD des resultats repetitifs pour la sorie individuelle
def fait_repetitives(csv_data, donnees, pid, province, questions, request):
    for i in donnees:
        ligne2 = ['Hospitalization card number ' + str(i)]
        csv_data.append(ligne2)
        for question in questions:
            ligne = [question.varname, question.questionen]
            donnee = Resultatrepetntp2.objects.filter(personne__id=pid, question_id=question.id,
                                                      assistant__id=request.user.id, fiche=i)
            if donnee:
                reponse = fait_reponse(donnee[0].reponsetexte, question, province)
                ligne.append(reponse)
            else:
                ligne.append('-')
            csv_data.append(ligne)


# Fait les reponses pour sortie individuelle
def fait_reponse(reponsetexte, question, province):
    if question.typequestion.nom == 'CATEGORIAL':
        resultat = Reponsentp2.objects.get(question=question.id,reponse_valeur=reponsetexte).__str__()
    elif question.typequestion.nom == 'DICHO' or question.typequestion.nom == 'DICHOU':
        resultat = CHOIX_ONUK[int(reponsetexte)]
    elif question.typequestion.nom == 'ETABLISSEMENT':
        resultat = Etablissement.objects.get(province__id=province,reponse_valeur=reponsetexte).__str__()
    elif question.typequestion.nom == 'MUNICIPALITE':
        resultat = Municipalite.objects.get(province__id=province, reponse_valeur=reponsetexte).__str__()
    else:
        resultat = reponsetexte
    return resultat


## Prepare les syntaxes pour exportation / importation des donnees pour les stats
# Pour les syntaxes SPSS, fait le fichier des variables et des listes de valeurs
def fait_entete_ntp2_spss(request, questionnaire, province):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSPSS_{}.sps"'.format(questionnaire)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions, usersntp2 = extraction_requete_ntp2(questionnaire)

    t = loader.get_template('spss_ntp2_syntaxe.txt')
    response.write(t.render({'questions': questions, 'users': usersntp2, 'province': province}))
    return response


# Pour les syntaxes STATA, fait le fichier des variables et des listes de valeurs
def fait_entete_ntp2_stata(request, questionnaire, province):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSTATA_{}.txt"'.format(questionnaire)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions, usersntp2 = extraction_requete_ntp2(questionnaire)
    typepresents = Questionntp2.objects.values('typequestion__nom').order_by().filter(questionnaire_id=questionnaire). \
                                            exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                            annotate(tqcount=Count('typequestion__nom'))

    t = loader.get_template('stata_ntp2_syntaxe.txt')
    response.write(t.render({'questions': questions, 'typequestions': typepresents, 'users': usersntp2, 'province': province}))
    return response


# Prepare la liste des questions du questionnaire selectionne et la liste des assistants du projet
def extraction_requete_ntp2(questionnaire):
    questions = Questionntp2.objects.filter(questionnaire_id=questionnaire). \
                                    exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                    order_by('questionno')
    usersntp2 = [{'id': p.user.id, 'username': p.user.username} for p in Projet.objects.filter(projet=Projet.NTP2)]

    return questions,  usersntp2


## Première étape pour exporter les données par province et questionnaire.
# Scinde les données en paquets de 100 dossiers si nécessaire
# appele par csv/<int:province>/<int:questionnaire>
@login_required(login_url=settings.LOGIN_URI)
def prepare_csv(request, province, questionnaire):
    province_nom = LISTE_PROVINCE[province]
    nombre_personnes = Personne.objects.filter(province_id=province).count()
    questionnaire_nom = Questionnaire.objects.get(pk=questionnaire)
    seuil = 100
    if nombre_personnes > seuil:
        reste = 0
        if nombre_personnes % seuil > 0:
            reste = 1
        iterations = int(nombre_personnes/seuil) + reste
    else:
        iterations = 1
    return render(request, 'page_extraction.html',
                      {
                       'iterations': range(iterations),
                       'province': province,
                       'questionnaire': questionnaire,
                       'questionnaire_nom': questionnaire_nom.nom_en,
                       'province_nom': province_nom,
                       'seuil': seuil
                      })


# Procede a l'exportation des donnees en CSV tab separated par province et questionnaire.
# Necessite d'utiliser le streaming pour exporter les données
def ffait_csv(request, province, questionnaire, iteration, seuil):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    questions = Questionntp2.objects.\
                        filter(questionnaire_id=questionnaire).\
                        exclude(Q(typequestion=7) | Q(typequestion=100)).\
                        order_by('questionno').values('id', 'varname')
    usersntp = [{'id': p.user.id} for p in Projet.objects.filter(projet=Projet.NTP2)]
    usersprovince = [{'id': p.user.id} for p in Profile.objects.filter(province=province)]
    liste = [i for i in usersntp for j in usersprovince if i['id'] == j['id']]
    inf = iteration * seuil
    sup = (iteration + 1) * seuil
    personnes = Personne.objects.filter(province_id=province).values('id', 'code')[inf:sup]
    toutesleslignes = []
    entete = ['ID', 'code', 'Assistant']
    if questionnaire > 1000:
        entete.append('Card')
    for question in questions:
        entete.append(question['varname'])
    toutesleslignes.append(entete)
    for assistant in liste:
        for personne in personnes:
            decompte = 0
            if questionnaire > 1000:
                donnees = Resultatrepetntp2.objects.order_by(). \
                                        filter(personne_id=personne['id'], assistant_id=assistant['id'], questionnaire_id=questionnaire). \
                                        values_list('fiche', flat=True).distinct()
                if donnees.count() > 0:
                    ligne = []
                    decompte = 0
                    for card in donnees:
                            ligne, decompte = fait_csv_repetitive(personne['id'], personne['code'], assistant['id'], questions, card, questionnaire)
            else:
                if Resultatntp2.objects.filter(personne_id=personne['id'], assistant_id=assistant['id']).exists():
                    ligne = [personne['id'], personne['code'], assistant['id']]
                    for question in questions:
                        try:
                            donnee = Resultatntp2.objects.filter(personne_id=personne['id'], question_id=question['id'],
                                                                 assistant_id=assistant['id']).values('reponsetexte')
                        except Resultatntp2.DoesNotExist:
                            donnee = None
                        if donnee:
                            ligne.append(donnee[0]['reponsetexte'])
                            decompte += 1
                        else:
                            ligne.append('')
            if decompte > 3:
                toutesleslignes.append(ligne)
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    province_nom = LISTE_PROVINCE[province]
    filename = 'Datas_{}_{}_{}_L{}.csv'.format(province_nom, questionnaire, now, iteration)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                      content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response


# Fait les requetes dans la BD des resultatsrepetitifs pour la sorie csv de tous
def fait_csv_repetitive(personne, code, assistant, questions, card, questionnaire):
    if Resultatrepetntp2.objects.filter(personne_id=personne, assistant_id=assistant, questionnaire_id=questionnaire, fiche=card).exists():
        ligne = [personne, code, assistant, card]
        decompte = 0
        for question in questions:
            try:
                donnee = Resultatrepetntp2.objects.\
                            filter(personne_id=personne, assistant_id=assistant, questionnaire_id=questionnaire, question_id=question['id'], fiche=card).\
                            values('reponsetexte')

            except Resultatrepetntp2.DoesNotExist:
                donnee = None
            if donnee:
                ligne.append(donnee[0]['reponsetexte'])
                decompte += 1
            else:
                ligne.append('')
    return ligne, decompte


