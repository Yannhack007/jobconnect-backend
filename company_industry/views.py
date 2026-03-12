from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Industry
from .serializers import IndustrySerializer

# Create your views here.
class IndustryListCreateView(generics.ListCreateAPIView):
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]
    queryset = Industry.objects.all()
    
class IndustryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]