# cotisations/admin.py
from django.contrib import admin
from .models import Cycle


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ['numero', 'groupe', 'beneficiaire',
                    'date_debut', 'date_fin', 'montant_total', 'termine']
    list_filter = ['termine', 'groupe']
    list_editable = ['termine']
    search_fields = ['groupe__nom', 'beneficiaire__user__last_name']