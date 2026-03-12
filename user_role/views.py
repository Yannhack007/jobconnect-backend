from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Role
from .serializers import RoleSerializer
# Create your views here.

class RoleListCreateView(generics.ListCreateAPIView):
    queryset           = Role.objects.all()
    serializer_class   = RoleSerializer
    permission_classes = [IsAdminUser]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Role.objects.all()
    serializer_class   = RoleSerializer
    permission_classes = [IsAdminUser]