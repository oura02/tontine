# membres/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Groupe, Membre, Adhesion


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MembreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    nom_complet = serializers.SerializerMethodField()

    class Meta:
        model = Membre
        fields = ['id', 'user', 'nom_complet', 'telephone',
                  'adresse', 'profession', 'statut', 'date_inscription']

    def get_nom_complet(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class GroupeSerializer(serializers.ModelSerializer):
    nombre_membres = serializers.SerializerMethodField()
    createur_nom = serializers.CharField(
        source='createur.username', read_only=True
    )

    class Meta:
        model = Groupe
        fields = ['id', 'nom', 'description', 'montant_cotisation',
                  'frequence', 'statut', 'date_debut',
                  'date_creation', 'createur_nom', 'nombre_membres']

    def get_nombre_membres(self, obj):
        return obj.adhesions.filter(actif=True).count()


class AdhesionSerializer(serializers.ModelSerializer):
    membre_nom = serializers.CharField(
        source='membre.__str__', read_only=True
    )
    groupe_nom = serializers.CharField(
        source='groupe.nom', read_only=True
    )

    class Meta:
        model = Adhesion
        fields = ['id', 'membre', 'membre_nom', 'groupe',
                  'groupe_nom', 'date_adhesion', 'ordre_benefice', 'actif']