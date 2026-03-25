# cotisations/serializers.py
from rest_framework import serializers
from .models import Cycle
from membres.serializers import GroupeSerializer, MembreSerializer


class CycleSerializer(serializers.ModelSerializer):
    groupe_nom = serializers.CharField(source='groupe.nom', read_only=True)
    beneficiaire_nom = serializers.CharField(
        source='beneficiaire.__str__', read_only=True
    )
    nombre_paiements = serializers.SerializerMethodField()
    taux_recouvrement = serializers.SerializerMethodField()

    class Meta:
        model = Cycle
        fields = ['id', 'groupe', 'groupe_nom', 'numero',
                  'date_debut', 'date_fin', 'beneficiaire',
                  'beneficiaire_nom', 'montant_total', 'termine',
                  'nombre_paiements', 'taux_recouvrement']

    def get_nombre_paiements(self, obj):
        return obj.paiements.filter(statut='paye').count()

    def get_taux_recouvrement(self, obj):
        total = obj.paiements.count()
        if total == 0:
            return 0
        payes = obj.paiements.filter(statut='paye').count()
        return round((payes / total) * 100, 2)