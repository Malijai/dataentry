# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dataentry.models import Questionnaire, Reponsentp2, Resultatrepetntp2, Questionntp2, Violation, Etablissement, Municipalite
from dataentry.models import Personne, Resultatntp2
from django.conf import settings
from django.contrib.auth.decorators import login_required
import csv
from django.template import loader, Context
from django.http import HttpResponse, StreamingHttpResponse
from django.apps import apps
from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from dataentry.dataentry_constants import CHOIX_ONUK
#A necessite l'installation de reportlab (pip install reportlab)
import datetime


NOM_FICHIER_PDF = "NTP_Community.pdf"
TITRE = "NTP Community Data Entry Protocol"
PAGE_INFO = " Data protocol - Printed date: " + datetime.datetime.now().strftime('%Y/%m/%d')
PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()
DATE = datetime.datetime.now().strftime('%Y %b %d')


#Pour exportation en CSV

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@login_required(login_url=settings.LOGIN_URI)
def ffait_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    questions = Questionntp2.objects.filter(qstyle=1).order_by('questionnaire_id','questionno')
    personnes = Personne.objects.all()
    toutesleslignes = ([])
    #writer = csv.writer(response)
    entete = []
    entete.append('ID')
    for question in questions:
       entete.append(question.varname)

    #writer.writerow(entete)
    toutesleslignes.append(entete)
    for personne in personnes:
        ligne = [personne.code]
        for question in questions:
            donnee = Resultatntp2.objects.filter(pk=personne.id, question_id=question.id,assistant_id=1,)
            if donnee:
                ligne.append(donnee[0].reponsetexte)
            else:
                ligne.append('-')

        toutesleslignes.append(ligne)
        #writer.writerow([donnee for donnee in ligne])

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                     content_type="text/csv")
    response['donnes'] = 'attachment; filename="donnes.csv"'
    return response


#Exportation des questions en PDF
def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, TITRE)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 130, DATE)
    canvas.setFont('Helvetica',10)
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setLineWidth(0.5)
    canvas.line(0, 65, PAGE_WIDTH - 0, 65)
    canvas.drawString(inch, 0.70 * inch, "NTP Community / %s" % PAGE_INFO)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica',10)
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setLineWidth(0.5)
    canvas.line(0, 65, PAGE_WIDTH - 0, 65)
    canvas.drawString(inch, 0.70 * inch, "Page %d %s" % (doc.page, PAGE_INFO))
    canvas.restoreState()


@login_required(login_url=settings.LOGIN_URI)
def some_pdf(request,pk):
    fichier = 'QID_' + str(pk) + '_' + NOM_FICHIER_PDF
#    doc = SimpleDocTemplate("/tmp/{}".format(NOM_FICHIER_PDF))
    doc = SimpleDocTemplate("/tmp/{}".format(fichier))
    questionnaire=Questionnaire.objects.get(pk=pk)
    Story = [Spacer(1,1.5 * inch)]
    Story.append(Paragraph(questionnaire.nom_en, styles["Heading1"]))
    Story.append(Spacer(1, 0.5 * inch))
#    Story = [] # (si on ne veut pas de premiere page differente on ne met pas d'Espace en haut de la 1ere)
    style = styles['Code']
    bullettes = styles['Code']
#    articles_list = Article.objects.all()
#    for article in articles_list:
#    im = '<img src="media/images/pointblanc.jpg"/>'
    viol = 0
    for question in Questionntp2.objects.filter(questionnaire_id=pk):
#        if question.typequestion.nom == 'TITLE':
        if question.typequestion.nom == 'TITLE':
            ptext = "<b>{}</b>".format(question.questionen)
            Story.append(Spacer(1, 0.2 * inch))
            Story.append(Paragraph(ptext, styles["Heading3"]))
            Story.append(Paragraph(".&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Question text", styles["Normal"]))
        elif question.typequestion.nom == 'COMMENT':
            ptext = "<b>{}</b>".format(question.questionen)
            Story.append(Paragraph(ptext, styles["Heading4"]))
            Story.append(Paragraph(".&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Question text", styles["Normal"]))
        else:
            x = 15 - len(question.varname)
            espace = ''
            for i in range(0, x):
                espace = espace + '&nbsp;'
            bogustext = question.varname + espace + question.questionen
            p = Paragraph(bogustext, style)
            Story.append(p)
        if question.typequestion.nom == "DICHO" or question.typequestion.nom == "DICHON" or question.typequestion.nom == "DICHOU":
            liste = [(1, 'Yes'), (0, 'No'), (98, 'NA'), (99, 'Unknown')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "BOOLEAN":
            liste = [(1, 'Yes mentioned'), (3, 'maybe but not explicit'), (100, 'No not mentioned'), (98, 'NA'), (99, 'Unknown')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "COUR":
            liste = [(1, 'Municipal'), (2, 'Provincial'), (3, 'Superior'),]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "CATEGORIAL":
            liste = Reponsentp2.objects.filter(question_id=question.id )
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.reponse_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "HCR20" or question.typequestion.nom == "POSOLOGIE" or question.typequestion.nom == "VICTIME":
            typetable = {"HCR20": "hcr", "POSOLOGIE": "posologie", "VICTIME": "victime", }
            tableext = typetable[question.typequestion.nom]
            Klass = apps.get_model('dataentry', tableext)
            liste = Klass.objects.all()
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.nom_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "PAYS" or question.typequestion.nom == "LANGUE":
            bogustext = '&#124;' + '&nbsp;' * 20 + "Stat can list of Countries or Languages"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)
        elif question.typequestion.nom == "VIOLATION":
            viol = 1
            bogustext = '&#124;' + '&nbsp;' * 20 + "See VIOLATION CODES at the end of the document"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)
        elif question.typequestion.nom =="ETABLISSEMENT" or question.typequestion.nom == "MUNICIPALITE":
            bogustext = '&#124;' + '&nbsp;' * 20 + "List of available Hospitals or Courts in each province"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)
        elif question.typequestion.nom == "CODEDATE" or question.typequestion.nom == "CODESTRING":
            bogustext = '&#124;' + '&nbsp;' * 20 + "Data will be encrypted before saving"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)

    if viol == 1:
        ptext = "VIOLATION CODES"
        #Story.append(Spacer(1, 0.2 * inch))
        Story.append(PageBreak())
        Story.append(Paragraph(ptext, styles["Heading3"]))
        liste = Violation.objects.all()
        for list in liste:
            espace1 = '&nbsp;'*3 + '&#x00B7;'
            espace2 = '&nbsp;'*3
            bogustext = '&#124;' + espace1 + str(list.id) + espace2 + list.nom_en
            p = Paragraph(bogustext,  bullettes)
            Story.append(p)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    fs = FileSystemStorage("/tmp")
    with fs.open(fichier) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fichier)
    return response


def some_texte(request, pid):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    province = request.user.profile.province
    # The data is hard-coded here, but you could load it from a database or
    # some other source.

    personne = Personne.objects.get(pk=pid)
    csv_data = ([])
    debut = []
    debut.append('Province & File code')
    debut.append(personne.province.nom_en)
    debut.append(personne.code)
    csv_data.append(debut)
    questionnaires = Questionnaire.objects.filter(id__gt=1 )
    for questionnaire in questionnaires:
        questions = Questionntp2.objects.filter(qstyle=1, questionnaire_id=questionnaire.id).order_by('questionno')
        ligne2 = []
        ligne2.append(questionnaire.nom_en)
        csv_data.append(ligne2)
        if questionnaire.id != 2000:
            for question in questions:
                ligne = []
                ligne.append(question.varname)
                ligne.append(question.questionen)
                donnee = Resultatntp2.objects.filter(personne__id=pid, question__id=question.id, assistant_id=1, )
                if donnee:
                    reponse = fait_reponse(donnee[0].reponsetexte, question, province)
                    ligne.append(reponse)
                else:
                    ligne.append('-')
                csv_data.append(ligne)
        else:
            donnees = Resultatrepetntp2.objects.order_by().filter(personne__id=pid, assistant__id=request.user.id,
                                                                  questionnaire__id=2000).values_list('fiche', flat=True).distinct()
            compte = donnees.count()
            ligne2 = []
            ligne2.append(str(compte) + ' different hospitalizations')
            csv_data.append(ligne2)
            for i in donnees :
                ligne2 = []
                ligne2.append('Hospitalization card number ' + str(i))
                csv_data.append(ligne2)
                for question in questions:
                    ligne = []
                    ligne.append(question.varname)
                    ligne.append(question.questionen)
                    donnee = Resultatrepetntp2.objects.filter(pk=pid, question_id=question.id, assistant_id=1, fiche=i)
                    if donnee:
                        reponse = fait_reponse(donnee[0].reponsetexte, question, province)
                        ligne.append(reponse)
                    else:
                        ligne.append('-')
                    csv_data.append(ligne)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer,dialect="excel-tab")
    response = StreamingHttpResponse((writer.writerow(row) for row in csv_data),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="' + str(personne.code) + '.txt"'
    return response


def fait_reponse(reponsetexte, question, province):

    if question.typequestion.nom == 'CATEGORIAL':
        resultat = Reponsentp2.objects.get(question=question.id,reponse_valeur=reponsetexte).__str__()
    elif question.typequestion.nom == 'DICHO' or question.typequestion.nom  == 'DICHOU':
        resultat = CHOIX_ONUK[int(reponsetexte)]
    elif question.typequestion.nom == 'ETABLISSEMENT':
        resultat = Etablissement.objects.get(province__id=province,reponse_valeur=reponsetexte).__str__()
    elif question.typequestion.nom == 'MUNICIPALITE':
        resultat = Municipalite.objects.get(province__id=province, reponse_valeur=reponsetexte).__str__()
    else:
        resultat = reponsetexte
    return resultat






