from __future__ import unicode_literals
from django import template
import re
from django.apps import apps
from dataentry.models import Resultatrepetntp2, Reponsentp2
from django import forms

register = template.Library()

@register.simple_tag
def fait_table(qid,type, *args, **kwargs):
    #questid type
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"PROVINCE": "province", "PAYS": "pays", "LANGUE": "langue","VIOLATION": "violation"}
    tableext = typetable[type]
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry'', typetable[b])
    listevaleurs = Klass.objects.all()
    name = "q" + str(qid) + "Z_Z" + str(ordre)
    liste = [('','')]
    for valeur in listevaleurs:
       vid=str(valeur.id)
       if type == "VIOLATION":
           nen= vid + ' - ' + valeur.nom_en
       else:
            nen=valeur.nom_en
       liste.append((vid, nen))

    question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

    return question.render(name, defaultvalue)

@register.simple_tag
def fait_reponse(qid,b, *args, **kwargs):
    #Pour listes de valeurs specifiques a chaque question
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid,cible,relation=relation)

    listevaleurs = Reponsentp2.objects.filter(question__id=qid, )
    name = "q" + str(qid) + "Z_Z" + str(ordre)
    liste = []
    for valeur in listevaleurs:
        vid = valeur.reponse_valeur
        nen = valeur.reponse_en
        liste.append((vid, nen))
    liste.append(('',''))
    question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

#   return question.render(name, defaultvalue)
    return question.render(name, defaultvalue)

@register.simple_tag
def fait_table_valeurs(qid,type, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur (independant de la province)
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"HCR20": "hcr", "POSOLOGIE":"posologie", "VICTIME":"victime",}
    tableext = typetable[type]
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.all()
    name = "q" + str(qid) + "Z_Z" + str(ordre)
    liste = [('','')]
    for valeur in listevaleurs:
       vid=str(valeur.reponse_valeur)
       nen=valeur.nom_en
       liste.append((vid, nen))

    question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

    return question.render(name, defaultvalue)

@register.simple_tag
def fait_table_valeurs_prov(qid,type, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #et dont la liste depend de la province
    province =  kwargs['province']
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite",}
    tableext = typetable[type]
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.filter(province__id = province)
    name = "q" + str(qid) + "Z_Z" + str(ordre)
    liste = [('','')]
    for valeur in listevaleurs:
       vid=str(valeur.reponse_valeur)
       nen=valeur.nom_en
       liste.append((vid, nen))

    question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

    return question.render(name, defaultvalue)

@register.simple_tag
def fait_dichou(qid,type, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid,cible,relation=relation)
    name = "q" + str(qid) + "Z_Z" + str(ordre)
    if type == "DICHO":
        liste = [(1, 'Yes'),(0, 'No')]
        question = forms.RadioSelect(choices = liste, attrs={'id': IDCondition,'name': name, })
    elif type == "BOOLEAN":
        liste = [('', ''),(1, 'Yes mentioned'),(100, 'No not mentioned'),(3, 'maybe but not explicit'),(98, 'NA'), (99,'Unknown')]
        question = forms.Select(choices=liste, attrs={'id': IDCondition, 'name': name, })
    else:
        liste = [(1, 'Yes'),(0, 'No'),(98, 'NA'), (99,'Unknown')]
        question = forms.RadioSelect(choices=liste, attrs={'id': IDCondition, 'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))

@register.simple_tag
def fait_court(qid,type, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid) + "Z_Z" + str(ordre)

    liste = [(1, 'Municipal'), (2, 'Provincial'), (3, 'Superior')]
    question = forms.Select(choices=liste, attrs={'id': IDCondition, 'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_textechar(qid,type, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    IDCondition = fait_id(qid,cible,relation=relation)
    name = "q" + str(qid) + "Z_Z" + str(ordre)
    if type == 'STRING' or type == 'CODESTRING':
        question = forms.TextInput(attrs={'size': 10, 'id': IDCondition,'name': name,})
    else:
        question = forms.NumberInput(attrs={'size': 10, 'id': IDCondition,'name': name,})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_date(qid,b, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    an = ''
    mois = ''
    jour = ''
    defff = ''

    if Resultatrepetntp2.objects.filter(personne__id=personneid, assistant__id=assistant, question__id=qid,fiche=ordre).exists():
        ancienne = Resultatrepetntp2.objects.get(personne__id=personneid, assistant__id=assistant, question__id=qid,
                                            fiche=ordre)
        defff = ancienne.reponsetexte
        if defff:
            an, mois, jour = defff.split('-')

    IDCondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid) + "Z_Z" + str(ordre)

    years = {x : x for x in range(1910,2019)}
    years[''] = ''
    days = {x : x for x in range(1,32)}
    days[''] = ''
    months=(('',''),(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'Jun'),(7,'Jul'),(8,'Aug'),(9,'Sept'),(10,'Oct'),(11,'Nov'),(12,'Dec'))
    year = forms.Select(choices = years.items(), attrs={'id': IDCondition, 'name': name + '_year', })
    month = forms.Select(choices = months, attrs={ 'name': name + '_month' })
    day = forms.Select(choices = days.items(), attrs={'name': name + '_day' })
# #name=q69_year, id=row...
    return year.render(name + '_year' , an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)

#Utlitaires generaux
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def fait_default(personneid, qid, *args, **kwargs):
    ##fail la valeur par deffaut
    assistant = kwargs['assistant']
    ordre = kwargs['ordre']
    defff = ''

    if Resultatrepetntp2.objects.filter(personne__id=personneid, assistant__id=assistant, question__id=qid, fiche=ordre).exists():
        ancienne = Resultatrepetntp2.objects.get(personne__id=personneid, assistant__id=assistant, question__id=qid, fiche=ordre)
        defff = ancienne.reponsetexte

    return defff

def fait_defaultVide(personneid, qid, *args, **kwargs):
    ##fail la valeur par deffaut
    assistant = kwargs['assistant']
    ordre  = kwargs['ordre']
    defff = ''

    return defff

def enlevelisttag(texte):
    ## pour mettre les radiobutton sur une seule ligne
    texte = re.sub(r"(<ul[^>]*>)",r"", texte)
    texte = re.sub(r"(<li[^>]*>)",r"", texte)
    texte = re.sub(r"(</li>)",r"", texte)
    return re.sub(r"(</ul>)",r" ", texte)

def fait_id(qid, cible, *args, **kwargs):
    ##fail l'ID pour javascripts ou autre
    relation = kwargs['relation']

    IDCondition = ''
    if relation != '' and cible != '':
        IDCondition = 'row-' + str(qid) + 'X' +  str(relation) + 'X' +  str(cible)

    return IDCondition


@register.simple_tag
def fait_dateh(persid,province,*args, ** kwargs):
    ordre = kwargs['ordre']
    assistant = kwargs['assistant']
    datehosp = ''

    if Resultatrepetntp2.objects.filter(personne__id=persid, assistant__id=assistant, question_id=2001, fiche=ordre).exists():
        ancienne = Resultatrepetntp2.objects.get(personne__id=persid, assistant__id=assistant, question__id=2001, fiche=ordre)
        datehosp = ancienne.reponsetexte

    return '<h3>' + str(datehosp) + '</h3><b>Hospitalized on: ' + str(datehosp) + '</b>'
