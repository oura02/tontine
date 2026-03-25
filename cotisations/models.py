# cotisations/models.py
from django.db import models
from membres.models import Groupe, Membre


class Cycle(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='cycles')
    numero = models.IntegerField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    beneficiaire = models.ForeignKey(Membre, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='cycles_beneficiaire')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    termine = models.BooleanField(default=False)

    def __str__(self):
        return f"Cycle {self.numero} — {self.groupe}"

    class Meta:
        ordering = ['numero']
        unique_together = ['groupe', 'numero']
        verbose_name = 'Cycle'
        verbose_name_plural = 'Cycles'