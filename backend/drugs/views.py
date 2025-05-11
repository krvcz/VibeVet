from decimal import Decimal, InvalidOperation
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator
from common.metrics import track_metrics
from .models import Drug, CustomDrug
from .serializers import (
    DrugSerializer,
    CreateCustomDrugSerializer,
    CustomDrugSerializer,
    UpdateCustomDrugSerializer,
    DosageCalcInputSerializer,
    DosageCalcResultSerializer,
)
from .services.dosage_calculator_service import DosageCalculatorService
import logging

logger = logging.getLogger('drugs')

@method_decorator(gzip_page, name='list')
@method_decorator(track_metrics('drug_list'), name='list')
class DrugListView(GenericViewSet, ListModelMixin):
    """
    API endpoint for retrieving a paginated list of drugs.
    Supports filtering by name or active ingredient.
    """
    serializer_class = DrugSerializer
    queryset = Drug.objects.all().select_related('species', 'measurement_unit', 'per_weight_unit')
    filter_backends = [SearchFilter]
    search_fields = ['name', 'active_ingredient']


@method_decorator(gzip_page, name='list')
@method_decorator(track_metrics('custom_drug_list'), name='list')
@method_decorator(track_metrics('custom_drug_create'), name='create')
@method_decorator(track_metrics('custom_drug_detail_retrieve'), name='retrieve')
@method_decorator(track_metrics('custom_drug_detail_update'), name='update')
@method_decorator(track_metrics('custom_drug_detail_destroy'), name='destroy')
class CustomDrugDetailView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    """List
    API endpoint for managing a specific custom drug.
    Supports GET, PUT, PATCH, and DELETE operations.
    Only the owner can access or modify their custom drugs.
    """
    queryset = CustomDrug.objects.select_related('species', 'measurement_unit', 'per_weight_unit')
    filter_backends = [SearchFilter]
    search_fields = ['name', 'active_ingredient']

    def get_serializer_class(self):
        """Use different serializers for different operations."""
        if self.action in ['update', 'partial_update']:
            return UpdateCustomDrugSerializer
        elif self.action == 'create':
            return CreateCustomDrugSerializer
        return CustomDrugSerializer
    
    def filter_queryset(self, queryset):
        """
        Filter the queryset based on the search parameter.
        Only for list action.
        """
        if self.action == 'list':
            for backend in list(self.filter_backends):
                queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_authenticated:
            return queryset.none()

        if not user.is_superuser:
            queryset = queryset.filter(user=user)

        if self.action == 'list':
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def perform_update(self, serializer):   
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this drug.")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this drug.")
        instance.delete()

@method_decorator(track_metrics('calculate_dosage'), name='create')
class DosageCalculatorView(GenericViewSet, CreateModelMixin):
    """
    API view for calculating drug dosage based on input parameters.
    """

    serializer_class = DosageCalcInputSerializer


    def create(self, request):
        """
        Calculate drug dosage with unit conversion support.
        """
        # Validate input
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        instance = input_serializer.save()
 
        output_serializer = DosageCalcResultSerializer(data=instance)
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


