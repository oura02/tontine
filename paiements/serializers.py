# paiements/serializers.py
from rest_framework import serializers
from .models import Paiement, Benefice
from membres.serializers import MembreSerializer, GroupeSerializer
import uuid


class PaiementSerializer(serializers.ModelSerializer):
    membre_nom = serializers.CharField(
        source='membre.__str__', read_only=True
    )
    groupe_nom = serializers.CharField(
        source='groupe.nom', read_only=True
    )

    class Meta:
        model = Paiement
        fields = ['id', 'membre', 'membre_nom', 'groupe', 'groupe_nom',
                  'cycle', 'montant', 'statut', 'moyen_paiement',
                  'date_echeance', 'date_paiement', 'reference',
                  'commentaire', 'date_creation']
        read_only_fields = ['date_creation', 'reference']

    def create(self, validated_data):
        validated_data['reference'] = str(uuid.uuid4())[:8].upper()
        return super().create(validated_data)

    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant doit etre superieur a 0."
            )
        return value


class BeneficeSerializer(serializers.ModelSerializer):
    membre_nom = serializers.CharField(
        source='membre.__str__', read_only=True
    )

    class Meta:
        model = Benefice
        fields = ['id', 'membre', 'membre_nom', 'cycle',
                  'montant', 'date_versement', 'verse']