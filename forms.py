# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Personne


class PersonneDob(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ('pid_sddob', 'completed')
