from __future__ import unicode_literals
from django import template
import re
from django.apps import apps
from dataentry.models import Listevaleur, Typequestion, Victime, Reponsentp2
from dataentry.dataentry_constants import CHOIX_ONUK, CHOIX_ON

register = template.Library()


@register.simple_tag
def spss_ntp_dichou(type, stats, *args, **kwargs):
    if type == "DICHO":
        liste = CHOIX_ON.items()
    else:
        liste = CHOIX_ONUK.items()
    return fait_ntp_rendu(liste, stats)


@register.simple_tag
def spss_ntp_table_valeurs_prov(type, stats, province,*args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #et dont la liste depend de la province
    typetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite",}
    tableext = typetable[type]

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.all().filter(province_id=province)
    liste = spss_ntp_liste_tables(listevaleurs, 'reponse')
    return fait_ntp_rendu(liste, stats)


@register.simple_tag
def spss_ntp_table_victime(stats, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur (independant de la province)
    listevaleurs = Victime.objects.all()
    liste = spss_ntp_liste_tables(listevaleurs, 'reponse')
    return fait_ntp_rendu(liste, stats)


@register.simple_tag
def spss_ntp_reponse(qid, stats, *args, **kwargs):
    #Pour listes de valeurs specifiques a chaque question
    listevaleurs = Reponsentp2.objects.filter(question_id=qid, )
    liste = spss_ntp_liste_tables(listevaleurs, 'reponse')
    return fait_ntp_rendu(liste, stats)


@register.simple_tag
def spss_ntp_liste_tables(listevaleurs, type):
    liste = []
    for valeur in listevaleurs:
        if type == 'reponse':
            val = valeur.reponse_valeur
            nen = valeur.reponse_en
            liste.append((val, nen))
        elif type == 'violation':
            val = str(valeur.reponse_valeur)
            nen = val + ' - ' + valeur.reponse_en
            liste.append((val, nen))
    return liste


@register.simple_tag
def spss_ntp_table(type, stats, *args, **kwargs):
    #questid type
    typeq = Typequestion.objects.get(nom=type)
    listevaleurs = Listevaleur.objects.filter(typequestion=typeq)
    if type == "VIOLATION":
        liste = spss_ntp_liste_tables(listevaleurs, 'violation')
    else:
        liste = spss_ntp_liste_tables(listevaleurs, 'reponse')
    return fait_ntp_rendu(liste, stats)


@register.simple_tag
def fait_ntp_rendu(liste, stats):
    sortie = ''
    if stats == 'stata':
        nb = len(liste)
        for i, val in enumerate(liste, 1):
            sortie += '{} "{}"  '. format(val[0], val[1])
            if i == nb:
                sortie += "\n"
    else:
        nb = len(liste)
        for i, val in enumerate(liste, 1):
            sortie += '{}        "{}"'. format(val[0], val[1])
            if i == nb:
                sortie += "/\n."
            else:
                sortie += "\n"
    return sortie


@register.simple_tag
def fait_ntp_ras(liste, stats):
    sortie = ''
    if stats == 'stata':
        nb = len(liste)
        for i, user in enumerate(liste, 1):
            sortie += '{} "{}"  '. format(user['id'], user['username'])
            if i == nb:
                sortie += "\n"
    else:
        nb = len(liste)
        for i, user in enumerate(liste, 1):
            sortie += '{}        "{}"'. format(user['id'], user['username'])
            if i == nb:
                sortie += "/\n."
            else:
                sortie += "\n"
    return sortie
