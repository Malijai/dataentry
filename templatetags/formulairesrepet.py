from __future__ import unicode_literals
from django import template
import re
from django.apps import apps
from dataentry.models import Resultatrepetntp2, Reponsentp2, Questionntp2
from django import forms
from .formulairesntp2 import fait_select_date, fait_liste_tables, enlevelisttag
from dataentry.dataentry_constants import CHOIX_ONUK, CHOIX_ON, CHOIX_BOOLEAN

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
    name = 'q{}Z_Z{}'.format(qid, ordre)
    if type == "VIOLATION":
        liste = fait_liste_tables(listevaleurs, 'violation')
    else:
        liste = fait_liste_tables(listevaleurs, 'id')

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
    name = 'q{}Z_Z{}'.format(qid, ordre)
    liste = fait_liste_tables(listevaleurs, 'reponse')

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
    name = 'q{}Z_Z{}'.format(qid, ordre)
    liste = fait_liste_tables(listevaleurs, 'nom')

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
    name = 'q{}Z_Z{}'.format(qid, ordre)
    liste = fait_liste_tables(listevaleurs, 'nom')

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
    name = 'q{}Z_Z{}'.format(qid, ordre)
    if type == "DICHO":
        liste = CHOIX_ON.items()
        question = forms.RadioSelect(choices = liste, attrs={'id': IDCondition,'name': name, })
    elif type == "BOOLEAN":
        # Choix normand plus que booleen
        liste = CHOIX_BOOLEAN.items()
        question = forms.Select(choices=liste, attrs={'id': IDCondition, 'name': name, })
    else:
        liste = CHOIX_ONUK.items()
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
    name = 'q{}Z_Z{}'.format(qid, ordre)

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
    name = 'q{}Z_Z{}'.format(qid, ordre)
    if type == 'STRING' or type == 'CODESTRING':
        question = forms.TextInput(attrs={'size': 30, 'id': IDCondition,'name': name,})
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': IDCondition,'name': name,})

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
    if Resultatrepetntp2.objects.filter(personne__id=personneid, assistant__id=assistant, question__id=qid,fiche=ordre).exists():
        ancienne = Resultatrepetntp2.objects.get(personne__id=personneid, assistant__id=assistant, question__id=qid,
                                            fiche=ordre).__str__()
        if ancienne:
            an, mois, jour = ancienne.split('-')

    IDCondition = fait_id(qid, cible, relation=relation)
    name = 'q{}Z_Z{}'.format(qid, ordre)
    day, month, year = fait_select_date(IDCondition, name)
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
    ancienne = ''

    if Resultatrepetntp2.objects.filter(personne__id=personneid, assistant__id=assistant, question__id=qid, fiche=ordre).exists():
        ancienne = Resultatrepetntp2.objects.get(personne__id=personneid, assistant__id=assistant,
                                                 question__id=qid, fiche=ordre).__str__()

    return ancienne


def fait_id(qid, cible, *args, **kwargs):
    ##fail l'ID pour javascripts ou autre
    relation = kwargs['relation']

    IDCondition = ''
    if relation != '' and cible != '':
        IDCondition = 'row-{}X{}X{}'.format(qid, relation, cible)
    return IDCondition


@register.simple_tag
def fait_dateh(persid,province,*args, ** kwargs):
    ordre = kwargs['ordre']
    assistant = kwargs['assistant']

    datehosp = ''
    question = Questionntp2.objects.get(typequestion_id=60, questionnaire_id=2000).pk
    if Resultatrepetntp2.objects.filter(personne__id=persid, assistant__id=assistant, question_id=question, fiche=ordre).exists():
        datehosp = Resultatrepetntp2.objects.get(personne__id=persid, assistant__id=assistant,
                                                 question__id=question, fiche=ordre).__str__()
    else:
        datehosp = ordre

    return '<h3>{}</h3><b>Hospitalized on: {}</b>'.format(datehosp, datehosp)

