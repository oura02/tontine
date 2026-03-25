# membres/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Groupe, Membre, Adhesion
from .serializers import GroupeSerializer, MembreSerializer, AdhesionSerializer


class GroupeViewSet(viewsets.ModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['statut', 'frequence']
    search_fields = ['nom', 'description']
    ordering_fields = ['date_creation', 'nom']

    def perform_create(self, serializer):
        serializer.save(createur=self.request.user)

    @action(detail=True, methods=['get'])
    def membres(self, request, pk=None):
        groupe = self.get_object()
        adhesions = groupe.adhesions.filter(actif=True)
        membres = [a.membre for a in adhesions]
        serializer = MembreSerializer(membres, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistiques(self, request, pk=None):
        groupe = self.get_object()
        total_membres = groupe.adhesions.filter(actif=True).count()
        total_paiements = groupe.paiements.filter(statut='paye').count()
        total_collecte = sum(
            p.montant for p in groupe.paiements.filter(statut='paye')
        )
        return Response({
            'groupe': groupe.nom,
            'total_membres': total_membres,
            'total_paiements': total_paiements,
            'total_collecte': float(total_collecte),
            'montant_cotisation': float(groupe.montant_cotisation),
        })


class MembreViewSet(viewsets.ModelViewSet):
    queryset = Membre.objects.select_related('user')
    serializer_class = MembreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['statut']
    search_fields = ['user__first_name', 'user__last_name', 'telephone']

    @action(detail=True, methods=['get'])
    def groupes(self, request, pk=None):
        membre = self.get_object()
        adhesions = membre.adhesions.filter(actif=True)
        groupes = [a.groupe for a in adhesions]
        serializer = GroupeSerializer(groupes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def historique_paiements(self, request, pk=None):
        membre = self.get_object()
        from paiements.models import Paiement
        from paiements.serializers import PaiementSerializer
        paiements = Paiement.objects.filter(membre=membre)
        serializer = PaiementSerializer(paiements, many=True)
        return Response(serializer.data)


class AdhesionViewSet(viewsets.ModelViewSet):
    queryset = Adhesion.objects.select_related('membre', 'groupe')
    serializer_class = AdhesionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['groupe', 'membre', 'actif']