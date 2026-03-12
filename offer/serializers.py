"""
Offer DTOs (Data Transfer Objects)
Separation claire Request/Response pour chaque endpoint
"""
from rest_framework import serializers
from .models import Offer


# ═══════════════════════════════════════════════════════════════
# OFFER DTOs
# ═══════════════════════════════════════════════════════════════

class CreateOfferRequestDTO(serializers.ModelSerializer):
    """DTO pour la requête de création d'offre (POST)"""
    
    class Meta:
        model = Offer
        fields = [
            'title',
            'description',
            'company',
            'location',
            'minsalary',
            'maxsalary',
            'responsibilities',
            'requirements',
            'type',
            'experience_level',
            'category',
            
            
        ]

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Title cannot be empty.')
        return value.strip()

    def validate_responsibilities(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Responsibilities must be a list.')
        if not value:
            raise serializers.ValidationError('At least one responsibility is required.')
        return [item.strip() for item in value if item.strip()]

    def validate_requirements(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Requirements must be a list.')
        if not value:
            raise serializers.ValidationError('At least one requirement is required.')
        return [item.strip() for item in value if item.strip()]

    def validate(self, attrs):
        # Vérifier que le salaire minimum est inférieur au maximum
        minsalary = attrs.get('minsalary')
        maxsalary = attrs.get('maxsalary')
        
        if minsalary and maxsalary and minsalary > maxsalary:
            raise serializers.ValidationError({
                'maxsalary': 'Maximum salary must be greater than minimum salary.'
            })

        # Validation des types d'offres
        valid_types = ['full-time', 'part-time', 'contract', 'internship', 'freelance']
        if attrs.get('type') and attrs['type'] not in valid_types:
            raise serializers.ValidationError({
                'type': f'Type must be one of: {", ".join(valid_types)}'
            })

        # Validation des niveaux d'expérience
        valid_levels = ['entry', 'junior', 'mid', 'senior', 'lead', 'executive']
        if attrs.get('experience_level') and attrs['experience_level'] not in valid_levels:
            raise serializers.ValidationError({
                'experience_level': f'Experience level must be one of: {", ".join(valid_levels)}'
            })

        return attrs


class UpdateOfferRequestDTO(serializers.ModelSerializer):
    """DTO pour la requête de mise à jour d'offre (PATCH/PUT)"""
    
    class Meta:
        model = Offer
        fields = [
            'title',
            'description',
            'company',
            'location',
            'minsalary',
            'maxsalary',
            'responsibilities',
            'requirements',
            'type',
            'experience_level',
            'category',
            
            'is_active',
            
        ]

    def validate_responsibilities(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise serializers.ValidationError('Responsibilities must be a list.')
            return [item.strip() for item in value if item.strip()]
        return value

    def validate_requirements(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise serializers.ValidationError('Requirements must be a list.')
            return [item.strip() for item in value if item.strip()]
        return value

    def validate(self, attrs):
        # Vérifier que le salaire minimum est inférieur au maximum
        minsalary = attrs.get('minsalary', self.instance.minsalary if self.instance else None)
        maxsalary = attrs.get('maxsalary', self.instance.maxsalary if self.instance else None)
        
        if minsalary and maxsalary and minsalary > maxsalary:
            raise serializers.ValidationError({
                'maxsalary': 'Maximum salary must be greater than minimum salary.'
            })

        return attrs


class OfferResponseDTO(serializers.ModelSerializer):
    """DTO pour la réponse d'une offre (GET detail)"""
    
    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'description',
            'company',
            'location',
            'minsalary',
            'maxsalary',
            'responsibilities',
            'requirements',
            'type',
            'experience_level',
            'posted_at',
            'category',
            
            'is_active',
            
        ]
        read_only_fields = ['id', 'posted_at']


class OfferListResponseDTO(serializers.ModelSerializer):
    """DTO pour la liste des offres (GET list) - Version allégée"""
    
    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'company',
            'location',
            'minsalary',
            'maxsalary',
            'type',
            'experience_level',
            'posted_at',
            'category',
            'is_active',
            
        ]
        read_only_fields = fields


class OfferSummaryDTO(serializers.ModelSerializer):
    """DTO ultra-léger pour les suggestions/recherches rapides"""
    
    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'company',
            'location',
            'type',
            'posted_at',
        ]
        read_only_fields = fields


# ═══════════════════════════════════════════════════════════════
# BACKWARD COMPATIBILITY
# ═══════════════════════════════════════════════════════════════

# Alias pour compatibilité avec ancien code
OfferSerializer = OfferResponseDTO