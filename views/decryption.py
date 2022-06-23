# -*- coding: utf-8 -*-
from django.http import HttpResponse, StreamingHttpResponse
from dataentry.models import Personne
from django.conf import settings
import datetime
#import logging
import csv
from dataentry.encrypter import Encrypter
from dataentry.dataentry_constants import LISTE_PROVINCE


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


def lisdob(nom_fichier_entree, nom_fichier_sortie):
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

# Pour l'exportation en streaming du CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value


#Pour decrypter dans la BD
def lissecret(request, prov):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="secret.txt"'
    e = Encrypter()
    private_key = e.read_key('myprivatekeyNTP2.pem')
    personnes = Personne.objects.filter(province_id=prov, completed=1)
    #pid_sed = models.TextField(blank=True, null=True)
    #pid_nam = models.TextField(blank=True, null=True)
    #pid_sddob = models.TextField(blank=True, null=True)
    toutesleslignes = []
    entete = ['ID', 'sed', 'nam', 'dob']
    toutesleslignes.append(entete)
    for personne in personnes:
        ligne = [personne.code]
        #ligne.append(personne.code)
        if personne.pid_sed != '':
            sed = Encrypter().decrypt(personne.pid_sed, private_key)
        else:
            sed = ""
        ligne.append(sed)
        if personne.pid_nam != '':
            nam = Encrypter().decrypt(personne.pid_nam, private_key)
        else:
            nam = ""
        ligne.append(nam)
        if personne.pid_sddob != '':
            sddob = Encrypter().decrypt(personne.pid_sddob, private_key)
        else:
            sddob = ""
        ligne.append(sddob)
        toutesleslignes.append(ligne)

    province_nom = LISTE_PROVINCE[prov]
    filename = 'SecretData_{}.csv'.format(province_nom)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                      content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response

