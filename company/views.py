from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer

class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]  # Allow unrestricted access for listing and creating companies
    
    def get_queryset(self):
        queryset = Company.objects.all()
        industry = self.request.query_params.get('industry')
        if industry is not None:
            queryset = queryset.filter(industry__iexact=industry)
        return queryset
    
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]  # Allow unrestricted access for retrieving, updating, and deleting companies