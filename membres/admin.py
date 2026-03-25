# membres/admin.py
from django.contrib import admin
from .models import Groupe, Membre, Adhesion


@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'montant_cotisation', 'frequence', 'statut', 'date_debut']
    list_filter = ['statut', 'frequence']
    search_fields = ['nom']


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'telephone', 'profession', 'statut']
    list_filter = ['statut']
    search_fields = ['user__first_name', 'user__last_name', 'telephone']


@admin.register(Adhesion)
class AdhesionAdmin(admin.ModelAdmin):
    list_display = ['membre', 'groupe', 'ordre_benefice', 'actif']
    list_filter = ['actif', 'groupe']
    list_editable = ['ordre_benefice', 'actif']