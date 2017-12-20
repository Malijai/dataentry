from __future__ import unicode_literals
from django import template
import re
from django.apps import apps
from dataentry.models import Resultat, Reponsentp2, Questionntp2, Resultatntp2
from django import forms

register = template.Library()


@register.simple_tag
def fait_dichou(a,b, *args, **kwargs):
    qid = a
    type = b
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']

    defaultvalue = fait_default(personneid, qid, vid, aid, assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    if type == "DICHO":
        liste = [(1, 'Yes'),(0, 'No')]
    else:
        liste = [(1, 'Yes'),(0, 'No'),(98, 'NA'), (99,'Unknown')]
    name = "q" + str(qid)
    question = forms.RadioSelect(choices = liste, attrs={'id': IDCondition,'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_date(qid,b, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']
    an = ''
    mois = ''
    jour = ''
    defff = ''
    existe = Resultat.objects.filter(personne__id = personneid, question__id = qid, assistant__id = assistant, verdict__id = vid, audience__id = aid).count()
    if existe > 0:
        ancienne = Resultat.objects.get(personne__id = personneid, question__id = qid, assistant__id = assistant, verdict__id = vid, audience__id = aid)
        defff = ancienne.reponsetexte
        an, mois, jour = defff.split('-')

    IDCondition = fait_id(qid,cible,relation=relation)
    name = "q" + str(qid)

    years = {x:x for x in  [''] + range(1910,2019)}
    days = {x:x for x in  [''] + range(1,32)}
    months=(('',''),(1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'Jun'),(7,'Jul'),(8,'Aug'),(9,'Sept'),(10,'Oct'),(11,'Nov'),(12,'Dec'))
    year = forms.Select(choices = years.iteritems(), attrs={'id': IDCondition, 'name': name + '_year', })
    month = forms.Select(choices = months, attrs={ 'name': name + '_month' })
    day = forms.Select(choices = days.iteritems(), attrs={'name': name + '_day' })
#name=q69_year, id=row...

    return year.render(name + '_year' , an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def fait_textechar(qid,type, *args, **kwargs):

    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    #assistant=1
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']

    defaultvalue = fait_default(personneid, qid, vid, aid, assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    name = "q" + str(qid)

    if type == 'STRING' or type == 'CODESTRING':
        question = forms.TextInput(attrs={'size': 10, 'id': IDCondition,'name': name,})
    else:
        question = forms.NumberInput(attrs={'size': 10, 'id': IDCondition,'name': name,})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_table(qid,type, *args, **kwargs):
    #questid type
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"PROVINCE": "province", "PAYS": "pays", "LANGUE": "langue","VIOLATION": "violation"}
    tableext = typetable[type]
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']

    defaultvalue = fait_default(personneid, qid, vid, aid, assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry'', typetable[b])
    listevaleurs = Klass.objects.all()
    name = "q" + str(qid)
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
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']

    defaultvalue = fait_default(personneid, qid, vid, aid, assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    listevaleurs = Reponsentp2.objects.filter(question_id=qid, )
    nombrelistevaleurs = Reponsentp2.objects.filter(question_id=qid).count()
    name = "q" + str(qid)
    liste = []
    for valeur in listevaleurs:
        vid = valeur.reponse_valeur
        nen = valeur.reponse_en
        liste.append((vid, nen))
    if nombrelistevaleurs < 5:
        question = forms.RadioSelect(choices=liste, attrs={'id': IDCondition, 'name': name, })
    else:
        liste.append(('',''))
        question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

#   return question.render(name, defaultvalue)
    return enlevelisttag(question.render(name, defaultvalue))

@register.simple_tag
def fait_table_valeurs(qid,type, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur (independant de la province)
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"HCR20": "hcr", "POSOLOGIE":"posologie", "VICTIME":"victime",}
    tableext = typetable[type]
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']

    defaultvalue = fait_default(personneid, qid, vid, aid, assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.all()
    name = "q" + str(qid)
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
    vid = kwargs['Vid']
    aid = kwargs['Aid']
    assistant = kwargs['uid']

    defaultvalue = fait_default(personneid, qid, vid, aid, assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.filter(province__id = province)
    name = "q" + str(qid)
    liste = [('','')]
    for valeur in listevaleurs:
       vid=str(valeur.reponse_valeur)
       nen=valeur.nom_en
       liste.append((vid, nen))

    question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

    return question.render(name, defaultvalue)


#Utlitaires generaux
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def enlevelisttag(texte):
    ## pour mettre les radiobutton sur une seule ligne
    texte = re.sub(r"(<ul[^>]*>)",r"", texte)
    texte = re.sub(r"(<li[^>]*>)",r"", texte)
    texte = re.sub(r"(</li>)",r"", texte)
    return re.sub(r"(</ul>)",r" ", texte)


def fait_default(personneid, qid, vid, aid, *args, **kwargs):
    ##fail la valeur par deffaut
    assistant = kwargs['assistant']
    defff = ''
    existe = Resultatntp2.objects.filter(personne__id=personneid, question__id=qid, assistant__id=assistant,verdict__id=vid, audience__id=aid).count()
    if existe > 0:
        ancienne = Resultatntp2.objects.get(personne__id=personneid, question__id=qid, assistant__id=assistant,verdict__id=vid, audience__id=aid)
        defff = ancienne.reponsetexte

    return defff


def fait_id(qid, cible, *args, **kwargs):
    ##fail l'ID pour javascripts ou autre
    relation = kwargs['relation']

    IDCondition = "q" + str(qid)
    if relation != '' and cible != '':
        IDCondition = 'row-' + str(qid) + 'X' +  str(relation) + 'X' +  str(cible)

    return IDCondition
