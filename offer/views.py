from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Offer
from .serializers import (
    CreateOfferRequestDTO,
    UpdateOfferRequestDTO,
    OfferResponseDTO,
    OfferListResponseDTO
)


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for job offers
    Requires JWT authentication for create/update/delete
    Public read access for list/retrieve
    """
    queryset = Offer.objects.filter(is_active=True).order_by('-posted_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return CreateOfferRequestDTO
        elif self.action in ['update', 'partial_update']:
            return UpdateOfferRequestDTO
        elif self.action == 'list':
            return OfferListResponseDTO
        return OfferResponseDTO
    
    def get_permissions(self):
        """
        Allow public read access (list, retrieve)
        Require authentication for write operations
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        """Create a new offer (only for authenticated recruiters)"""
        # Check if user is a recruiter
        if not hasattr(request.user, 'role') or request.user.role != 'recruteur':
            return Response(
                {'error': 'Only recruiters can create job offers.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            offer = serializer.save()
            response_serializer = OfferResponseDTO(offer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update an existing offer"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            offer = serializer.save()
            response_serializer = OfferResponseDTO(offer)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)