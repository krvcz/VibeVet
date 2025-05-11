from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet
from .models import Species, Unit
from .serializers import SpeciesSerializer, UnitSerializer

class SpeciesListView(generics.ListAPIView):
    """API view to list all animal species"""
    queryset: QuerySet[Species] = Species.objects.all()
    serializer_class = SpeciesSerializer
    permission_classes = [IsAuthenticated]
    
class UnitListView(generics.ListAPIView):
    """API view to list all measurement units"""
    queryset: QuerySet[Unit] = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
