# paiements/models.py
from django.db import models
from membres.models import Membre, Groupe
from cotisations.models import Cycle


class Paiement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('en_retard', 'En retard'),
        ('annule', 'Annulé'),
    ]

    MOYEN_CHOICES = [
        ('especes', 'Espèces'),
        ('mobile_money', 'Mobile Money'),
        ('virement', 'Virement'),
        ('cheque', 'Chèque'),
    ]

    membre = models.ForeignKey(Membre, on_delete=models.CASCADE,
                               related_name='paiements')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE,
                               related_name='paiements')
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE,
                              related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES,
                              default='en_attente')
    moyen_paiement = models.CharField(max_length=15, choices=MOYEN_CHOICES,
                                      default='especes')
    date_echeance = models.DateField()
    date_paiement = models.DateTimeField(null=True, blank=True)
    reference = models.CharField(max_length=50, unique=True, blank=True)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.membre} — {self.groupe} — {self.montant} FCFA"

    class Meta:
        ordering = ['-date_echeance']
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'


class Benefice(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE,
                               related_name='benefices')
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE,
                              related_name='benefices')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_versement = models.DateTimeField(null=True, blank=True)
    verse = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membre} — {self.montant} FCFA"

    class Meta:
        ordering = ['-date_versement']
        verbose_name = 'Benefice'
        verbose_name_plural = 'Benefices'