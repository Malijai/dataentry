from __future__ import unicode_literals
from django.contrib import admin

from .models import Typequestion, Questionnaire, Questionntp2, Personne, Reponsentp2


class QuestionAdmin(admin.ModelAdmin):
    # admin.site.site_header = 'My admin'
    list_display = ('questionno', 'questionen')
    list_filter = ['questionnaire', 'typequestion']

    def save_model(self, request, obj, form, change):
        obj.save()


class PersonneAdmin(admin.ModelAdmin):
    list_display = ('code', 'hospcode', 'province', 'assistant','completed')
    list_filter = ['selecthosp', 'province', 'assistant', 'completed']
    actions = ['ouvre_dossier']

    def ouvre_dossier(self, request, queryset):
        rows_updated = queryset.update(completed='')
        if rows_updated == 1:
            message_bit = "1 dossier a été"
        else:
            message_bit = "%s dossiers ont été" % rows_updated
        self.message_user(request, "%s réouvert(s)." % message_bit)
    ouvre_dossier.short_description = "Réouvrir les dossiers cochés"

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(Typequestion)
admin.site.register(Questionnaire)
admin.site.register(Questionntp2, QuestionAdmin)
admin.site.register(Personne, PersonneAdmin)
admin.site.register(Reponsentp2)
