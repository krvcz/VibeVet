from rest_framework import serializers

from common.services import rating_service
from .models import Rating, Species, Unit

class SpeciesSerializer(serializers.ModelSerializer):
    """Serializer for Species model"""
    class Meta:
        model = Species
        fields = ['id', 'name', 'description']

class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model"""
    class Meta:
        model = Unit
        fields = ['id', 'name', 'short_name']

class RatingSerializer(serializers.Serializer):
    rating = serializers.ChoiceField(
        choices=[('up', 'up'), ('down', 'down')],
        help_text="Choose 'up' for positive rating or 'down' for negative."
    )

    def save(self, **kwargs):
        interaction = self.instance
        rating = self.validated_data['rating']
        user = self.context['request'].user

        # Use the generic rating service
        rating_service.rate_content(
            content_object=interaction,
            rating=self.validated_data['rating'],
            user=user, **kwargs
        ) 
        return interaction