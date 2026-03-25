# membres/models.py
from django.db import models
from django.contrib.auth.models import User


class Groupe(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('termine', 'Terminé'),
        ('suspendu', 'Suspendu'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    montant_cotisation = models.DecimalField(max_digits=10, decimal_places=2)
    frequence = models.CharField(max_length=20, choices=[
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
    ], default='mensuel')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateField()
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupes_crees')

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Groupe'
        verbose_name_plural = 'Groupes'


class Membre(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membre')
    telephone = models.CharField(max_length=20)
    adresse = models.TextField(blank=True)
    profession = models.CharField(max_length=100, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ['user__last_name']
        verbose_name = 'Membre'
        verbose_name_plural = 'Membres'


class Adhesion(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='adhesions')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='adhesions')
    date_adhesion = models.DateTimeField(auto_now_add=True)
    ordre_benefice = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.membre} — {self.groupe}"

    class Meta:
        unique_together = ['membre', 'groupe']
        ordering = ['ordre_benefice']
        verbose_name = 'Adhesion'
        verbose_name_plural = 'Adhesions'