from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


DEFAULT_UID = 1
# met tous les utilisateurs par defaut a 1 (maliadmin)

#######################
## listes de valeurs typequestion_id=13 (PROVINCE)
class Province(models.Model):
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    estimatedcases = models.IntegerField(blank=True, null=True)
    reelcases = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.reponse_en


class Personne(models.Model):
    code = models.CharField(max_length=200,)
    hospcode = models.CharField(max_length=250)
    selecthosp = models.CharField(max_length=250)
    date_indexh = models.DateTimeField(blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    completed = models.CharField(max_length=200, blank=True, null=True)
    assistant = models.ForeignKey(User, default=DEFAULT_UID, on_delete=models.DO_NOTHING)
    pid_sed = models.TextField(blank=True, null=True)
    pid_nam = models.TextField(blank=True, null=True)
    pid_sddob = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['province', 'code']

    def __str__(self):
        return '%s' % self.code


##   listes valeurs dependantes des provinces
DEFAULT_PID = 1


class Etablissement(models.Model):
    #   listes de valeurs typequestion_id=9 (ETABLISSEMENT)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province, default=DEFAULT_PID, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['reponse_en']

    def __str__(self):
        return '%s' % self.reponse_en


class Municipalite(models.Model):
    #   listes de valeurs typequestion_id=15 (MUNICIPALITE)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province, default=DEFAULT_PID, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['reponse_en']

    def __str__(self):
        return '%s' % self.reponse_en


## Definit la forme html des questions ainsi que le type de réponse attendu (texte, bool, date etc)
class Typequestion(models.Model):
    nom = models.CharField(max_length=200, )
    tatable = models.CharField(max_length=200, blank=True, null=True)
    taille = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom


##   listes valeurs non dependantes des provinces SANS province
class Listevaleur(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['typequestion', 'reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en


class Victime(models.Model):
    #  listes de valeurs typequestion_id=14 (VICTIME)
    #   Restee a part a cause de la logique du tri des items
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.reponse_en


class Questionnaire(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom_en


#######################
## Questions utilisees pour tous les questionnaires
# Parent_ID permet de lier l'affichage conditionnel d'une question en fonction de la réponse précédente
# à la question dont l'ID=Parent_id via la relation établie par  le champ relation et la valeur cible prédéfinie
# (par exemple question 2 s'ouvrira si question 1 (parent_id) a comme réponse 998 (cible) avec relation égale)
DEFAULT_PARENT_ID = 1


class Questionntp2(models.Model):
    questionno = models.IntegerField()
    questionen = models.CharField(max_length=255,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey("self", default=DEFAULT_PARENT_ID, on_delete=models.DO_NOTHING)
    relation = models.CharField(blank=True, null=True, max_length=45,)
    cible = models.CharField(blank=True, null=True, max_length=45,)
    varname = models.CharField(blank=True, null=True, max_length=45,)
    aidefr = models.TextField(blank=True, null=True)
    aideen = models.TextField(blank=True, null=True)
    qstyle = models.CharField(blank=True, null=True, max_length=45,)
    parentvarname = models.CharField(blank=True, null=True, max_length=45,)

    class Meta:
        ordering = ['questionno']

    def __str__(self):
        return '%s' % self.questionen


#######################
## listes de valeurs des questions de typequestion_id=4 (CATEGORIAL)
# Pour les questions qui aparaissent rarement et dont les réponses sont des listes de valeur
class Reponsentp2(models.Model):
    question = models.ForeignKey(Questionntp2, on_delete=models.DO_NOTHING)
    reponse_no = models.CharField(max_length=200)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    varname = models.CharField(blank=True, null=True, max_length=45,)

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en


#######################
## Enregistrement des reponses des donnees NON repetitives
class Resultatntp2(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    question = models.ForeignKey(Questionntp2, on_delete=models.CASCADE)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # constraints = [models.UniqueConstraint(fields=['personne', 'assistant', 'question'], name='unique_result')]
        unique_together = (('personne', 'assistant', 'question'),)
        indexes = [models.Index(fields=['personne', 'assistant', 'question'])]

    def __str__(self):
        return '%s' % self.reponsetexte


#######################
## Enregistrement des reponses des donnees REPETITIVES
# Garder le questionnaire_id pour pouvoir effacer une fiche au complet sans faire une requete compliquée
DEFAULT_DATE = '0000-00-00'


class Resultatrepetntp2(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaire, db_index=True, on_delete=models.DO_NOTHING)
    fiche = models.IntegerField(db_index=True)
    question = models.ForeignKey(Questionntp2, db_index=True, on_delete=models.CASCADE)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # constraints = [models.UniqueConstraint(fields=['personne', 'assistant', 'questionnaire', 'question', 'fiche'], name='unique_repet')]
        unique_together = ('personne', 'assistant', 'questionnaire', 'question', 'fiche')
        ordering = ['personne', 'assistant', 'questionnaire', 'question', 'fiche']
        indexes = [models.Index(fields=['personne', 'assistant', 'questionnaire', 'question', 'fiche'])]


    def __str__(self):
        return '%s' % self.reponsetexte


############################################

