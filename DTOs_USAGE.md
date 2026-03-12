# Architecture DTOs - Guide d'utilisation

## 📋 Vue d'ensemble

Ce projet utilise une architecture **Request/Response DTOs** (Data Transfer Objects) pour une séparation claire entre les données entrantes (Request) et sortantes (Response).

### Avantages
✅ **Sécurité** : Contrôle strict des données entrantes/sortantes  
✅ **Validation** : Règles métier claires et testables  
✅ **Documentation** : API auto-documentée (Swagger)  
✅ **Maintenance** : Changements isolés par endpoint  

---

## 🔐 Authentication DTOs

### 1. **Login** (POST /api/auth/login/)

**Request:**
```python
from authentication.serializers import LoginRequestDTO

serializer = LoginRequestDTO(data=request.data)
if serializer.is_valid():
    user = serializer.validated_data['user']
    # Générer tokens JWT...
```

**Payload:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```python
from authentication.serializers import LoginResponseDTO

response_data = {
    'access': access_token,
    'refresh': refresh_token,
    'user': user
}
serializer = LoginResponseDTO(response_data)
return Response(serializer.data)
```

**Response JSON:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhb...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhb...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "chercheur",
    "is_recruiter": false,
    "is_job_seeker": true
  }
}
```

---

### 2. **Register** (POST /api/auth/register/)

**Request:**
```python
from authentication.serializers import RegisterRequestDTO, RegisterResponseDTO

serializer = RegisterRequestDTO(data=request.data)
if serializer.is_valid():
    user = serializer.save()
    response_serializer = RegisterResponseDTO({
        'message': 'User created successfully',
        'user': user
    })
    return Response(response_serializer.data, status=201)
```

**Payload (Chercheur):**
```json
{
  "email": "jobseeker@example.com",
  "password": "securePass123",
  "password_confirm": "securePass123",
  "full_name": "Jane Smith",
  "role": "chercheur"
}
```

**Payload (Recruteur):**
```json
{
  "email": "recruiter@company.com",
  "password": "securePass123",
  "password_confirm": "securePass123",
  "full_name": "John Recruiter",
  "company_name": "Tech Corp",
  "role": "recruteur"
}
```

---

### 3. **Refresh Token** (POST /api/auth/refresh/)

**Request:**
```python
from authentication.serializers import RefreshTokenRequestDTO, RefreshTokenResponseDTO

serializer = RefreshTokenRequestDTO(data=request.data)
if serializer.is_valid():
    # Générer nouveau access token...
    response = RefreshTokenResponseDTO({'access': new_access_token})
    return Response(response.data)
```

---

## 👤 User DTOs

### 1. **Get User Profile** (GET /api/users/me/)

**Response:**
```python
from authentication.serializers import UserResponseDTO

serializer = UserResponseDTO(request.user)
return Response(serializer.data)
```

**Response JSON:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "company_name": null,
  "role": "chercheur",
  "is_recruiter": false,
  "is_job_seeker": true,
  "provider": "email",
  "is_active": true,
  "created_at": "2026-03-09T10:30:00Z",
  "updated_at": "2026-03-09T10:30:00Z"
}
```

---

### 2. **Update User Profile** (PATCH /api/users/me/)

**Request:**
```python
from authentication.serializers import UpdateUserRequestDTO, UserResponseDTO

serializer = UpdateUserRequestDTO(
    request.user,
    data=request.data,
    partial=True
)
if serializer.is_valid():
    user = serializer.save()
    response = UserResponseDTO(user)
    return Response(response.data)
```

**Payload:**
```json
{
  "full_name": "John Updated Doe",
  "company_name": "New Company"
}
```

---

### 3. **List Users** (GET /api/users/)

**Response:**
```python
from authentication.serializers import UserListResponseDTO
from rest_framework.pagination import PageNumberPagination

users = User.objects.filter(is_active=True)
paginator = PageNumberPagination()
page = paginator.paginate_queryset(users, request)
serializer = UserListResponseDTO(page, many=True)
return paginator.get_paginated_response(serializer.data)
```

---

### 4. **Change Password** (POST /api/users/change-password/)

**Request:**
```python
from authentication.serializers import ChangePasswordRequestDTO

serializer = ChangePasswordRequestDTO(
    data=request.data,
    context={'request': request}
)
if serializer.is_valid():
    user = request.user
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({'message': 'Password changed successfully'})
```

**Payload:**
```json
{
  "old_password": "currentPass123",
  "new_password": "newSecurePass456",
  "new_password_confirm": "newSecurePass456"
}
```

---

## 💼 Offer DTOs

### 1. **Create Offer** (POST /api/offers/)

**Request:**
```python
from offer.serializers import CreateOfferRequestDTO, OfferResponseDTO

serializer = CreateOfferRequestDTO(data=request.data)
if serializer.is_valid():
    offer = serializer.save()
    response = OfferResponseDTO(offer)
    return Response(response.data, status=201)
```

**Payload:**
```json
{
  "title": "Senior Backend Developer",
  "description": "We are looking for an experienced backend developer...",
  "company_name": "Tech Solutions Inc",
  "location": "Paris, France",
  "minsalary": 50000.00,
  "maxsalary": 70000.00,
  "responsibilities": [
    "Design and develop scalable APIs",
    "Collaborate with frontend team",
    "Write clean, maintainable code"
  ],
  "requirements": [
    "5+ years Python experience",
    "Django/FastAPI expertise",
    "PostgreSQL knowledge"
  ],
  "type": "full-time",
  "experience_level": "senior",
  "category": "IT",
  "external_link": "https://company.com/jobs/123",
  "company_logo": "https://company.com/logo.png"
}
```

---

### 2. **Update Offer** (PATCH /api/offers/{id}/)

**Request:**
```python
from offer.serializers import UpdateOfferRequestDTO, OfferResponseDTO

offer = Offer.objects.get(id=offer_id)
serializer = UpdateOfferRequestDTO(
    offer,
    data=request.data,
    partial=True
)
if serializer.is_valid():
    updated_offer = serializer.save()
    response = OfferResponseDTO(updated_offer)
    return Response(response.data)
```

**Payload:**
```json
{
  "title": "Senior Backend Developer (Updated)",
  "maxsalary": 75000.00,
  "is_active": true
}
```

---

### 3. **Get Offer Detail** (GET /api/offers/{id}/)

**Response:**
```python
from offer.serializers import OfferResponseDTO

offer = Offer.objects.get(id=offer_id)
serializer = OfferResponseDTO(offer)
return Response(serializer.data)
```

**Response JSON:**
```json
{
  "id": 1,
  "title": "Senior Backend Developer",
  "description": "We are looking for...",
  "company_name": "Tech Solutions Inc",
  "location": "Paris, France",
  "minsalary": "50000.00",
  "maxsalary": "70000.00",
  "responsibilities": [
    "Design and develop scalable APIs",
    "Collaborate with frontend team"
  ],
  "requirements": [
    "5+ years Python experience",
    "Django/FastAPI expertise"
  ],
  "type": "full-time",
  "experience_level": "senior",
  "posted_at": "2026-03-09T10:00:00Z",
  "category": "IT",
  "external_link": "https://company.com/jobs/123",
  "is_active": true,
  "company_logo": "https://company.com/logo.png"
}
```

---

### 4. **List Offers** (GET /api/offers/)

**Response:**
```python
from offer.serializers import OfferListResponseDTO

offers = Offer.objects.filter(is_active=True).order_by('-posted_at')
serializer = OfferListResponseDTO(offers, many=True)
return Response(serializer.data)
```

**Response JSON:**
```json
[
  {
    "id": 1,
    "title": "Senior Backend Developer",
    "company_name": "Tech Solutions Inc",
    "location": "Paris, France",
    "minsalary": "50000.00",
    "maxsalary": "70000.00",
    "type": "full-time",
    "experience_level": "senior",
    "posted_at": "2026-03-09T10:00:00Z",
    "category": "IT",
    "is_active": true,
    "company_logo": "https://company.com/logo.png"
  }
]
```

---

### 5. **Search Offers (Summary)** (GET /api/offers/search/)

**Response:**
```python
from offer.serializers import OfferSummaryDTO

offers = Offer.objects.filter(title__icontains=query)
serializer = OfferSummaryDTO(offers, many=True)
return Response(serializer.data)
```

---

## 🔄 Backward Compatibility

Pour éviter de casser le code existant, des **aliases** sont définis:

```python
# authentication/serializers.py
AuthenticationSerializer = LoginRequestDTO
LoginSerializer = LoginRequestDTO
RegisterSerializer = RegisterRequestDTO
UserSerializer = UserResponseDTO

# offer/serializers.py
OfferSerializer = OfferResponseDTO
```

---

## 🛡️ Validations intégrées

### Authentication
- ✅ Email unique et format valide
- ✅ Mot de passe minimum 8 caractères
- ✅ Confirmation de mot de passe
- ✅ Nom d'entreprise obligatoire pour recruteurs
- ✅ Compte actif pour login

### Offers
- ✅ Salaire max > salaire min
- ✅ Responsabilités et exigences = listes non vides
- ✅ Type d'offre parmi valeurs autorisées
- ✅ Niveau d'expérience validé
- ✅ Titre non vide

---

## 📝 Exemple de ViewSet complet

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from offer.models import Offer
from offer.serializers import (
    CreateOfferRequestDTO,
    UpdateOfferRequestDTO,
    OfferResponseDTO,
    OfferListResponseDTO,
    OfferSummaryDTO
)

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOfferRequestDTO
        elif self.action in ['update', 'partial_update']:
            return UpdateOfferRequestDTO
        elif self.action == 'list':
            return OfferListResponseDTO
        elif self.action == 'search':
            return OfferSummaryDTO
        return OfferResponseDTO

    def create(self, request):
        serializer = CreateOfferRequestDTO(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = serializer.save()
        response_serializer = OfferResponseDTO(offer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        offer = self.get_object()
        serializer = OfferResponseDTO(offer)
        return Response(serializer.data)

    def list(self, request):
        offers = self.get_queryset().filter(is_active=True)
        serializer = OfferListResponseDTO(offers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        offers = self.get_queryset().filter(title__icontains=query)
        serializer = OfferSummaryDTO(offers, many=True)
        return Response(serializer.data)
```

---

## 🚀 Prochaines étapes

1. Créer les views/viewsets utilisant ces DTOs
2. Configurer les URLs
3. Ajouter les permissions (IsAuthenticated, IsRecruiter, etc.)
4. Intégrer avec Swagger/drf-yasg pour documentation API
5. Écrire les tests unitaires pour chaque DTO
