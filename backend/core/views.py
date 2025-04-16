import logging
from datetime import datetime
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response 
from rest_framework import status
from django.db.models import Q, QuerySet
from django.views.decorators.gzip import gzip_page
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .metrics import track_metrics
from .models import Drug, Species, MeasurementUnit, CustomDrug, DrugInteraction, TreatmentGuide, UserSearchHistory
from .utils import PaginatedResponse
from .serializers import (
    DrugSerializer, 
    CreateCustomDrugSerializer, 
    CustomDrugSerializer,
    UpdateCustomDrugSerializer,
    CreateDrugInteractionSerializer,
    DrugInteractionSerializer,
    RateDrugInteractionSerializer,
    DosageCalcInputSerializer,
    DosageCalcResultSerializer,
    CreateTreatmentGuideSerializer,
    TreatmentGuideSerializer,
    RateTreatmentGuideSerializer,
    UserSearchHistorySerializer
)
from .services import (
    custom_drug_service,
    drug_interaction_service,
    rating_service,
    search_history_service
)
from .services.dosage_calculator_service import calculate_dosage, DosageCalculationError
from .services.treatment_guide_service import (
    create_treatment_guide,
    TreatmentGuideValidationError,
    TreatmentGuideProcessingError,
    rate_treatment_guide
)

logger = logging.getLogger('core')

@method_decorator(gzip_page, name='get')
@method_decorator(track_metrics('drug_list'), name='get')
@method_decorator(csrf_exempt, name='dispatch')
class DrugListView(ListAPIView):
    """
    API endpoint for retrieving a paginated list of drugs.
    Supports filtering by name or active ingredient.
    """
    serializer_class = DrugSerializer
    queryset = Drug.objects.all().select_related(
        'species', 
        'measurement_target'
    ).order_by('name')

    def filter_queryset(self, queryset: QuerySet[Drug]) -> QuerySet[Drug]:
        """
        Filter the queryset based on the search parameter.
        Searches in both name and active_ingredient fields.
        """
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(active_ingredient__icontains=search)
            )
        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Get paginated list of drugs with optional search filter.
        
        Query Parameters:
            page (int): Page number (default: 1)
            limit (int): Number of items per page (default: 20, max: 100)
            search (str): Optional search term for filtering drugs
        """
        return PaginatedResponse.paginate(
            request=request,
            queryset=self.filter_queryset(self.get_queryset()),
            serializer_class=self.serializer_class
        )

@method_decorator(gzip_page, name='post')
@method_decorator(track_metrics('create_custom_drug'), name='post')
@method_decorator(csrf_exempt, name='dispatch')
class CreateCustomDrugView(CreateAPIView):
    """
    API endpoint for creating a new custom drug.
    Requires authenticated user.
    """
    serializer_class = CreateCustomDrugSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            custom_drug = custom_drug_service.create_custom_drug(
                data=serializer.validated_data,
                user=request.user
            )
            response_serializer = CustomDrugSerializer(custom_drug)
            return Response(
                response_serializer.data, 
                status=status.HTTP_201_CREATED
            )
            
        except (custom_drug_service.CustomDrugValidationError, ValidationError) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except (Species.DoesNotExist, MeasurementUnit.DoesNotExist) as e:
            logger.error("Resource not found: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            logger.error(
                "Unexpected error creating custom drug: %s",
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred while creating the custom drug"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(gzip_page, name='get')
@method_decorator(track_metrics('custom_drug_list'), name='get')
@method_decorator(csrf_exempt, name='dispatch')
class CustomDrugListView(ListAPIView):
    """
    API endpoint for retrieving a paginated list of custom drugs.
    Requires authenticated user. Returns only drugs owned by the requesting user.
    """
    serializer_class = CustomDrugSerializer
    queryset = CustomDrug.objects.select_related(
        'species',
        'measurement_target'
    ).order_by('-created_at')

    def filter_queryset(self, queryset: QuerySet[CustomDrug]) -> QuerySet[CustomDrug]:
        """Filter queryset based on search parameter."""
        search = self.request.query_params.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(active_ingredient__icontains=search)
            )
        return queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Get paginated list of custom drugs with optional search filter.
        
        Query Parameters:
            page (int): Page number (default: 1)
            limit (int): Number of items per page (default: 20, max: 100)
            search (str): Optional search term for filtering drugs
        """
        return PaginatedResponse.paginate(
            request=request,
            queryset=self.filter_queryset(self.get_queryset()),
            serializer_class=self.serializer_class
        )

@method_decorator(gzip_page, name='get')
@method_decorator(track_metrics('custom_drug_detail_get'), name='get')
@method_decorator(track_metrics('custom_drug_detail_put'), name='put')
@method_decorator(track_metrics('custom_drug_detail_patch'), name='patch')
@method_decorator(track_metrics('custom_drug_detail_delete'), name='delete')
@method_decorator(csrf_exempt, name='dispatch')
class CustomDrugDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for managing a specific custom drug.
    Supports GET, PUT, PATCH, and DELETE operations.
    Only the owner can access or modify their custom drugs.
    """
    serializer_class = CustomDrugSerializer
    queryset = CustomDrug.objects.select_related('species', 'measurement_target')

    def get_serializer_class(self):
        """Use different serializers for different operations."""
        if getattr(self, 'request', None) is not None and self.request.method in ['PUT', 'PATCH']:
            return UpdateCustomDrugSerializer
        return CustomDrugSerializer

    def update(self, request, *args, **kwargs):
        """Handle both PUT and PATCH requests."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        try:
            updated_drug = custom_drug_service.update_custom_drug(
                custom_drug=instance,
                data=request.data,
                user=request.user,
                partial=partial
            )
            serializer = CustomDrugSerializer(updated_drug)
            return Response(serializer.data)
            
        except custom_drug_service.CustomDrugValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(
                "Error updating custom drug %d: %s",
                instance.id,
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred while updating the custom drug"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """Handle DELETE requests."""
        instance = self.get_object()
        
        try:
            custom_drug_service.delete_custom_drug(
                custom_drug=instance,
                user=request.user
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            logger.error(
                "Error deleting custom drug %d: %s",
                instance.id,
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred while deleting the custom drug"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(track_metrics('create_drug_interaction'), name='post')
class CreateDrugInteractionView(CreateAPIView):
    """
    API endpoint for creating a new drug interaction query.
    """
    serializer_class = CreateDrugInteractionSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            interaction = drug_interaction_service.create_interaction(
                drug_ids=serializer.validated_data['drug_ids'],
                context=serializer.validated_data.get('context'),
                user=request.user
            )
            
            # Add to search history
            search_history_service.add_to_history(
                module='drug-interaction',
                query=f"Drug interaction query for drug IDs: {serializer.validated_data['drug_ids']}",
                user=request.user
            )
            
            response_serializer = DrugInteractionSerializer(interaction)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except drug_interaction_service.DrugInteractionValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(
                "Unexpected error creating drug interaction: %s",
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred while creating the drug interaction"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(track_metrics('rate_drug_interaction'), name='patch')
class RateDrugInteractionView(GenericAPIView):
    """
    API endpoint for rating a drug interaction (thumbs up/down).
    Allows users to rate drug interactions with thumbs up/down.
    """
    serializer_class = RateDrugInteractionSerializer
    queryset = DrugInteraction.objects.all()
    lookup_url_kwarg = 'interaction_id'
    lookup_field = 'id'

    def patch(self, request: Request, interaction_id: int) -> Response:
        """Rate a drug interaction with thumbs up/down."""
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Get the interaction object using get_object() from GenericAPIView
            interaction = self.get_object()
            
            # Use the generic rating service
            rating_service.rate_content(
                content_object=interaction,
                rating=serializer.validated_data['rating'],
                user=request.user
            )
            return Response(
                {"message": "Rating updated successfully"},
                status=status.HTTP_200_OK
            )
            
        except ObjectDoesNotExist as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
            
        except rating_service.RatingValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(
                "Unexpected error rating drug interaction %d: %s",
                interaction_id,
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred while rating the drug interaction"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(track_metrics('drug_interaction_list'), name='get')
class DrugInteractionListView(ListAPIView):
    """
    API endpoint for retrieving a paginated list of drug interactions.
    Returns interactions created by the authenticated user.
    """
    serializer_class = DrugInteractionSerializer
    queryset = DrugInteraction.objects.all().order_by('-created_at')

    def get_queryset(self) -> QuerySet[DrugInteraction]:
        """Filter queryset to only return interactions for the current user."""
        return self.queryset.filter(created_by=self.request.user)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Get paginated list of drug interactions.
        
        Query Parameters:
            page (int): Page number (default: 1)
            limit (int): Number of items per page (default: 20, max: 100)
        """
        return PaginatedResponse.paginate(
            request=request,
            queryset=self.get_queryset(),
            serializer_class=self.serializer_class
        )

@method_decorator(track_metrics('calculate_dosage'), name='post')
@method_decorator(csrf_exempt, name='dispatch')
class DosageCalculatorView(GenericAPIView):
    """
    API view for calculating drug dosage based on input parameters.
    """
    serializer_class = DosageCalcInputSerializer

    def post(self, request: Request) -> Response:
        """
        Calculate drug dosage based on provided parameters.
        
        Expected input:
        {
            "drug_id": number,
            "weight": number,
            "species": number,
            "target_unit": number
        }
        """
        try:
            # Validate input data
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                logger.warning("Invalid input data for dosage calculation: %s", serializer.errors)
                return Response(
                    {"error": "Invalid input data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate dosage using service
            result = calculate_dosage(**serializer.validated_data)
            
            # Add to search history
            search_history_service.add_to_history(
                module='dosage-calc',
                query=f"Dosage calculation for drug ID: {serializer.validated_data['drug_id']}, weight: {serializer.validated_data['weight']}",
                user=request.user
            )
            
            # Serialize and return result
            result_serializer = DosageCalcResultSerializer(result)
            return Response(result_serializer.data, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.warning("Validation error in dosage calculation: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DosageCalculationError as e:
            logger.warning("Dosage calculation failed: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            logger.error("Unexpected error in dosage calculation: %s", str(e), exc_info=True)
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(track_metrics('create_treatment_guide'), name='post')
class TreatmentGuideCreateView(GenericAPIView):
    """
    API endpoint for creating treatment guide queries based on diagnostic factors.
    Requires authenticated user.
    """
    serializer_class = CreateTreatmentGuideSerializer

    def post(self, request: Request) -> Response:
        """
        Create a treatment guide query based on provided diagnostic factors.
        
        Expected input:
        {
            "factors": {
                "temperature": "39.5",
                "heart_rate": "110",
                ...
            }
        }
        """
        try:
            # Validate input data
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                logger.warning("Invalid input data for treatment guide: %s", serializer.errors)
                return Response(
                    {"error": "Invalid input data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process treatment guide using service
            result = create_treatment_guide(
                factors=serializer.validated_data['factors'],
                user=request.user
            )
            
            # Add to search history
            search_history_service.add_to_history(
                module='treatment-guide',
                query=f"Treatment guide query with factors: {list(serializer.validated_data['factors'].keys())}",
                user=request.user
            )
            
            # Serialize and return result
            response_serializer = TreatmentGuideSerializer(result)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except TreatmentGuideValidationError as e:
            logger.warning("Treatment guide validation error: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TreatmentGuideProcessingError as e:
            logger.error("Treatment guide processing error: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error("Unexpected error in treatment guide creation: %s", str(e), exc_info=True)
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(track_metrics('rate_treatment_guide'), name='patch')
class RateTreatmentGuideView(GenericAPIView):
    """
    API endpoint for rating a treatment guide with thumbs up/down.
    Requires authenticated user.
    """
    serializer_class = RateTreatmentGuideSerializer
    queryset = TreatmentGuide.objects.all()
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def patch(self, request: Request, id: int) -> Response:
        """
        Rate a treatment guide with thumbs up/down.
        
        Args:
            id: ID of the treatment guide to rate
            
        Request body:
        {
            "rating": "up" | "down"
        }
        """
        try:
            # Validate input data
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                logger.warning("Invalid rating data: %s", serializer.errors)
                return Response(
                    {"error": "Invalid input data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the treatment guide object using get_object() from GenericAPIView
            treatment_guide = self.get_object()
            
            # Use the generic rating service
            rating_service.rate_content(
                content_object=treatment_guide,
                rating=serializer.validated_data['rating'],
                user=request.user
            )
            
            return Response(
                {"message": "Rating updated successfully"},
                status=status.HTTP_200_OK
            )
            
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Treatment guide with id {id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except rating_service.RatingValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                "Unexpected error rating treatment guide %d: %s",
                id,
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(track_metrics('search_history_list'), name='get')
class SearchHistoryListView(ListAPIView):
    """
    API endpoint for retrieving a paginated list of user's search history.
    Returns only search history for the authenticated user.
    Uses Row Level Security via UserSearchHistoryManager.
    """
    serializer_class = UserSearchHistorySerializer
    queryset = UserSearchHistory.objects.all()

    def get_queryset(self) -> QuerySet[UserSearchHistory]:
        """
        Filter queryset by optional parameters:
        - module
        - date range (from_date, to_date)
        Note: User filtering is handled by UserSearchHistoryManager's RLS.
        """
        queryset = self.queryset

        # Apply module filter if provided
        module = self.request.query_params.get('module', '').strip()
        if module:
            queryset = queryset.filter(module=module)
        
        # Apply date range filters if provided
        from_date = self.request.query_params.get('from_date')
        if from_date:
            try:
                datetime.fromisoformat(from_date.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__gte=from_date)
            except ValueError:
                logger.warning("Invalid from_date format: %s", from_date)
                
        to_date = self.request.query_params.get('to_date')
        if to_date:
            try:
                datetime.fromisoformat(to_date.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__lte=to_date)
            except ValueError:
                logger.warning("Invalid to_date format: %s", to_date)
        
        return queryset.order_by('-created_at')

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Get paginated list of search history with optional filters.
        
        Query Parameters:
            page (int): Page number (default: 1)
            limit (int): Number of items per page (default: 20, max: 100)
            module (str): Optional filter by module (e.g., "drug-interaction")
            from_date (str): Optional filter for entries after this date (ISO format)
            to_date (str): Optional filter for entries before this date (ISO format)
        """
        try:
            return PaginatedResponse.paginate(
                request=request,
                queryset=self.get_queryset(),
                serializer_class=self.serializer_class
            )
            
        except Exception as e:
            logger.error(
                "Unexpected error retrieving search history: %s",
                str(e),
                exc_info=True
            )
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
