from __future__ import unicode_literals
from django import template
import re
from django.apps import apps
from dataentry.models import Resultat, Reponse
from django import forms

register = template.Library()


@register.simple_tag
def fait_dichou(a,b, *args, **kwargs):
    qid = a
    type = b
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    if type == "DICHO":
        liste = [(1, 'Yes'),(0, 'No')]
    else:
        liste = [(1, 'Yes'),(0, 'No'),(98, 'NA'), (99,'Unknown')]
    name = "q" + str(qid)
    question = forms.RadioSelect(choices = liste, attrs={'id': IDCondition,'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_date(a,b, *args, **kwargs):
    qid = a
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    name = "q" + str(qid)
    question = forms.DateInput(format=('%d-%m-%Y'), attrs={'id': IDCondition,'name': name,})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_textechar(a,b, *args, **kwargs):
    qid = a
    type = b
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    name = "q" + str(qid)

    if type == 'STRING':
        question = forms.TextInput(attrs={'size': 10, 'id': IDCondition,'name': name,})
    else:
        question = forms.NumberInput(attrs={'size': 10, 'id': IDCondition,'name': name,})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_table(a,b, *args, **kwargs):
    #questid type
    qid = a
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"PROVINCE": "province", "PAYS": "pays", "LANGUE": "langue","VIOLATION": "violation"}
    tableext = typetable[b]
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry'', typetable[b])
    listevaleurs = Klass.objects.all()
    name = "q" + str(qid)
    liste = [('','')]
    for valeur in listevaleurs:
       vid=str(valeur.id)
       nen=valeur.nom_en
       liste.append((vid, nen))

    question = forms.Select(choices = liste, attrs={'id': IDCondition,'name': name, })

    return question.render(name, defaultvalue)

@register.simple_tag
def fait_reponse(a,b, *args, **kwargs):
    #Pour listes de valeurs specifiques a chaque question
    #questid type
    qid = a
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
    IDCondition = fait_id(qid,cible,relation=relation)

    listevaleurs = Reponse.objects.filter(question__id=qid, )
    nombrelistevaleurs = Reponse.objects.filter(question__id=qid).count()
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
def fait_table_valeurs(a,b, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur (independant de la province)
    qid = a
    province = b
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"HCR20": "hcr", "POSOLOGIE":"posologie", "VICTIME":"victime",}
    tableext = typetable[b]
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
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
def fait_table_valeurs_prov(a,b, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #et dont la liste depend de la province
    qid = a
    province =  kwargs['province']
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite",}
    tableext = typetable[b]
    assistant=1

    defaultvalue = fait_default(personneid,qid,assistant=assistant)
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


@register.filter
def enlevelisttag(texte):
    ## pour mettre les radiobutton sur une seule ligne
    texte = re.sub(r"(<ul[^>]*>)",r"", texte)
    texte = re.sub(r"(<li[^>]*>)",r"", texte)
    texte = re.sub(r"(</li>)",r"", texte)
    return re.sub(r"(</ul>)",r" ", texte)


@register.simple_tag
def fait_default(a,b, *args, **kwargs):
    ##fail la valeur par deffaut
    personneid = a
    qid=b
    assistant = kwargs['assistant']
#    province =  kwargs['province']
    defff = ''
    existe = Resultat.objects.filter(personne__id=personneid, question__id=qid, assistant__id=assistant).count()
    if existe > 0:
        ancienne = Resultat.objects.get(personne__id=personneid, question__id=qid, assistant__id=1)
        defff = ancienne.reponsetexte

    return defff

@register.simple_tag
def fait_id(a, b, *args, **kwargs):
    ##fail l'ID pour javascripts ou autre
    qid=a
    cible=b
    relation = kwargs['relation']

    IDCondition = "q" + str(qid)
    if relation != '' and cible != '':
        IDCondition = 'row-' + str(qid) + 'X' +  str(relation) + 'X' +  str(cible)

    return IDCondition