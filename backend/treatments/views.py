import logging
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import  CreateModelMixin
from common.metrics import track_metrics
from common.utils import exception_handler_decorator, with_exception_handling
from .models import TreatmentGuide
from .serializers import (
    CreateTreatmentGuideSerializer,
    TreatmentGuideSerializer,
    RateTreatmentGuideSerializer,
)
from common.services import rating_service
from users.services import search_history_service
from .services.treatment_guide_service import (
    create_treatment_guide,
    TreatmentGuideValidationError,
    TreatmentGuideProcessingError,
)

logger = logging.getLogger('treatments')

@method_decorator(track_metrics('create_treatment_guide'), name='create')
class TreatmentGuideCreateView(GenericViewSet, CreateModelMixin):
    """
    API endpoint for creating treatment guide queries based on diagnostic factors.
    Requires authenticated user.
    """
    serializer_class = CreateTreatmentGuideSerializer

    def create(self, request: Request) -> Response:
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = TreatmentGuideSerializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        # Check if this was a new creation or existing interaction
        if hasattr(serializer, 'is_existing') and serializer.is_existing:
            return Response(
                response_serializer.data, 
                status=status.HTTP_200_OK,
                headers=headers
            )
        
        return Response(
            response_serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    

    @action(
        detail=True, 
        methods=['patch'],
        url_path='rate',
        serializer_class=RateTreatmentGuideSerializer,
        queryset=TreatmentGuide.objects.all(),
    )
    @method_decorator(track_metrics('rate_treatment_guid'))
    def rate(self, request: Request, pk=None) -> Response:
        """Rate a treatment guide with thumbs up/down."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Rating updated successfully"},
            status=status.HTTP_200_OK
        )    
