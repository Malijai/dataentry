# -*- coding: utf-8 -*-
from django.http import HttpResponse
from dataentry.models import Personne
from django.conf import settings
import datetime
#import logging
from dataentry.encrypter import Encrypter


def decode_donnee(ciphertext):
    #PK_path = settings.PRIVATE_KEY_PATH
    #PK_name = settings.PRIVATE_KEY
    PK_path = settings.PUBLIC_KEY_PATH
    PK_name = settings.PRIVATE_KEY_NTP2
    e = Encrypter()
    private_key = e.read_key(PK_path + PK_name)
    decripted = e.decrypt(ciphertext, private_key)
    return decripted


def decrypt(request, pid):
    personne = Personne.objects.get(pk=pid)
    sddob = decode_donnee(personne.pid_sddob)
    #sed = decode_donnee(personne.pid_sed)
    #nam = decode_donnee(personne.pid_nam)
    #return HttpResponse("{} ; {} ; {} ; {}".format(pid, sddob, sed,nam))
    return HttpResponse("{} ; {}".format(pid, sddob))



def lis(nom_fichier_entree, nom_fichier_sortie):
    e = Encrypter()
    private_key = e.read_key('myprivatekeyNTP2.pem')
    with open(nom_fichier_entree) as entree:
        data = []
        for ligne in entree:
            champs = ligne.split('\t')
            d = champs[3]
            if champs[0] != '':
                ddn_decryptee = Encrypter().decrypt(d, private_key)
                data.append((champs[0], champs[1], ddn_decryptee))
                print(champs[0] + '\t' +  champs[1] +  '\t' + ddn_decryptee)

#dataentry_personneDDN.csv
