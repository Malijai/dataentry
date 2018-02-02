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
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)
    parent= models.ForeignKey("self", default=DEFAULT_PARENT_ID, on_delete=models.DO_NOTHING)
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
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    ddn = models.CharField(max_length=200,blank=True, null=True)
    diedon = models.CharField(max_length=200,blank=True, null=True)
    dod = models.CharField(max_length=200,blank=True, null=True)
    completed = models.CharField(max_length=200,blank=True, null=True)
    sexe = models.CharField(max_length=200,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    reponse_no = models.CharField(max_length=200)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)

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
    province = models.ForeignKey(Province,default=DEFAULT_PID, on_delete=models.DO_NOTHING)

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
    province = models.ForeignKey(Province,default=DEFAULT_PID, on_delete=models.DO_NOTHING)

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
    personne = models.ForeignKey(Personne, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    verdict = models.ForeignKey(Verdict, default=DEFAULT_VERD, on_delete=models.DO_NOTHING)
    audience = models.ForeignKey(Audience, default=DEFAULT_VERD, on_delete=models.DO_NOTHING)
    reponsetexte = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('personne', 'question','verdict','audience','assistant'),)


DEFAULT_PARENT_ID = 0
class Questionntp2(models.Model):
    questionno = models.IntegerField()
    questionen = models.CharField(max_length=255,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)
    parent= models.ForeignKey("self", default=DEFAULT_PARENT_ID, on_delete=models.DO_NOTHING)
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

class Reponsentp2(models.Model):
    question = models.ForeignKey(Questionntp2, on_delete=models.DO_NOTHING)
    reponse_no = models.CharField(max_length=200)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)

    class Meta:
       ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.nom_en

    def __unicode__(self):
        return u'%s' % self.nom_en


DEFAULT_VERD = 100
class Resultatntp2(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Questionntp2, on_delete=models.DO_NOTHING)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    verdict = models.ForeignKey(Verdict, default=DEFAULT_VERD, on_delete=models.DO_NOTHING)
    audience = models.ForeignKey(Audience, default=DEFAULT_VERD, on_delete=models.DO_NOTHING)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('personne', 'question','verdict','audience','assistant'),)


DEFAULT_DATE = '0000-00-00'
class Resultatrepetntp2(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.DO_NOTHING)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    questionnaire =  models.ForeignKey(Questionnaire,db_index=True, on_delete=models.DO_NOTHING)
    fiche = models.IntegerField(db_index=True)
    question = models.ForeignKey(Questionntp2, db_index=True, on_delete=models.DO_NOTHING)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = (('personne', 'assistant', 'questionnaire', 'question', 'fiche',))

        ordering = ['personne', 'assistant', 'questionnaire', 'fiche']
