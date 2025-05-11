import logging
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import  CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from common.metrics import track_metrics
from .models import DrugInteraction
from .serializers import (
    CreateDrugInteractionSerializer,
    DrugInteractionSerializer,
    RateDrugInteractionSerializer,
)

logger = logging.getLogger('interactions')

@method_decorator(track_metrics('create_drug_interaction'), name='create')
class DrugInteractionView(GenericViewSet, CreateModelMixin):
    """
    API endpoint for creating a new drug interaction query.
    """
    serializer_class = CreateDrugInteractionSerializer

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = DrugInteractionSerializer(instance)
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
        serializer_class=RateDrugInteractionSerializer,
        queryset=DrugInteraction.objects.all(),
    )
    @method_decorator(track_metrics('rate_drug_interaction'))
    def rate(self, request: Request, pk=None) -> Response:
        """Rate a drug interaction with thumbs up/down."""
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
    
    