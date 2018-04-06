# -*- coding: utf-8 -*-
from django.http import HttpResponse
from dataentry.models import Personne
from django.conf import settings
import datetime
#import logging
from dataentry.encrypter import Encrypter


def decode_donnee(ciphertext):
    PK_path = settings.PRIVATE_KEY_PATH
    PK_name =  settings.PRIVATE_KEY
    e = Encrypter()
    private_key = e.read_key(PK_path + PK_name)
    decripted = e.decrypt(ciphertext, private_key)
    return decripted


def decrypt(request, pid):
    personne = Personne.objects.get(pk=pid)
    sddob = decode_donnee(personne.pid_sddob)
    sed = decode_donnee(personne.pid_sed)
    nam = decode_donnee(personne.pid_nam)
    return HttpResponse("{} {} {}".format(sddob,sed,nam))