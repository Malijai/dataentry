from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class Typequestion(models.Model):
    nom = models.CharField(max_length=200, )
    table = models.CharField(max_length=200, blank=True, null=True)
    taille = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom

    def __unicode__(self):
        return u'%s' % self.nom


class Questionnaire(models.Model):
    nom_en = models.CharField(max_length=200,)
    nom_fr = models.CharField(max_length=200,)
    description = models.CharField(max_length=200,)

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

DEFAULT_PARENT_ID = 0
class Question(models.Model):
    questionno = models.IntegerField()
    questionen = models.CharField(max_length=255,)
    questionnaire = models.ForeignKey(Questionnaire)
    typequestion = models.ForeignKey(Typequestion)
    parent= models.ForeignKey("self", default=DEFAULT_PARENT_ID)
    relation = models.CharField(blank=True, null=True, max_length=45,)
    cible = models.CharField(blank=True, null=True, max_length=45,)
    varname = models.CharField(blank=True, null=True, max_length=45,)
    aidefr = models.TextField(blank=True, null=True)
    aideen = models.TextField(blank=True, null=True)
    qstyle = models.CharField(blank=True, null=True, max_length=45,)

    class Meta:
        ordering = ['questionno']

    def __str__(self):
        return '%s' % self.questionen

    def __unicode__(self):
        return u'%s' % self.questionen


class Province(models.Model):
    nom_en = models.CharField(max_length=200,)
    nom_fr = models.CharField(max_length=200,)

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en


class Pays(models.Model):
    nom_en = models.CharField(max_length=200,)
    nom_fr = models.CharField(max_length=200,)

    class Meta:
       ordering = ['nom_en']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

class Personne(models.Model):
    code = models.CharField(max_length=200,)
    province = models.ForeignKey(Province)
    ddn = models.CharField(max_length=200,blank=True, null=True)
    diedon = models.CharField(max_length=200,blank=True, null=True)
    dod = models.CharField(max_length=200,blank=True, null=True)
    completed = models.CharField(max_length=200,blank=True, null=True)
    sexe = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assistant = models.ForeignKey(User)


class Reponse(models.Model):
    question = models.ForeignKey(Question)
    reponse_no = models.CharField(max_length=200)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    questionnaire = models.ForeignKey(Questionnaire)

    class Meta:
       ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en


class Langue(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['nom_en']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en


class Violation(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

class Hcr(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

class Victime(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

class Posologie(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

DEFAULT_PID = 1
class Etablissement(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province,default=DEFAULT_PID)

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

class Municipalite(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province,default=DEFAULT_PID)

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en

class Verdict(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en


class Audience(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en


DEFAULT_VERD = 100
class Resultat(models.Model):
    personne = models.ForeignKey(Personne)
    question = models.ForeignKey(Question)
    assistant = models.ForeignKey(User)
    verdict = models.ForeignKey(Verdict, default=DEFAULT_VERD)
    audience = models.ForeignKey(Audience, default=DEFAULT_VERD)
    reponsetexte = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('personne', 'question','verdict','audience','assistant'),)

class AFSF(models.Model):
    personne = models.ForeignKey(Personne)
    assistant = models.ForeignKey(User)
    AFSF_order = models.IntegerField()
    AFSF1 = models.IntegerField(blank=True, null=True)
    AFSF2 = models.CharField(max_length=250, blank=True, null=True)
    AFSF3 = models.CharField(max_length=250, blank=True, null=True)
    AFSF2DATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF3DATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF5 = models.IntegerField(blank=True, null=True)
    AFSF9 = models.IntegerField(blank=True, null=True)
    AFSF9a = models.IntegerField(blank=True, null=True)
    AFSF9aDATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF9aL = models.IntegerField(blank=True, null=True)
    AFSF9b = models.IntegerField(blank=True, null=True)
    AFSF9bDATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF9bL = models.IntegerField(blank=True, null=True)
    AFSF9c = models.IntegerField(blank=True, null=True)
    AFSF9cDATE = models.CharField(max_length=250,blank=True, null=True)
    AFSF9cL = models.IntegerField(blank=True, null=True)
    AFSF9d = models.IntegerField(blank=True, null=True)
    AFSF9dDATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF9dL = models.IntegerField(blank=True, null=True)
    AFSF9e = models.IntegerField(blank=True, null=True)
    AFSF9eDATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF9eL = models.IntegerField(blank=True, null=True)
    AFSF18 = models.IntegerField(blank=True, null=True)
    AFSF18b = models.CharField(max_length=250, blank=True, null=True)
    AFSF18bDATE = models.CharField(max_length=250, blank=True, null=True)
    AFSF18A = models.IntegerField(blank=True, null=True)
    AFSF15 = models.IntegerField(blank=True, null=True)
    AFSF15A = models.IntegerField(blank=True, null=True)
    AFSF15B = models.IntegerField(blank=True, null=True)
    AFSF15C = models.IntegerField(blank=True, null=True)
    AFSF15D = models.IntegerField(blank=True, null=True)
    AFSF15E = models.IntegerField(blank=True, null=True)
    AFSF15F = models.IntegerField(blank=True, null=True)
    AFSF16A = models.CharField(max_length=250, blank=True, null=True)
    AFSF16B = models.CharField(max_length=250, blank=True, null=True)
    AFSF16C = models.CharField(max_length=250, blank=True, null=True)
    AFSF6 = models.IntegerField(blank=True, null=True)
    AFSF6A = models.IntegerField(blank=True, null=True)
    AFSF6B = models.IntegerField(blank=True, null=True)
    AFSF6C = models.IntegerField(blank=True, null=True)
    AFSF17 = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('personne','assistant','AFSF_order'))
