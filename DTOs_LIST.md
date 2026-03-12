# 📋 Liste complète des DTOs disponibles

## 🔐 Authentication DTOs (`authentication/serializers.py`)

### Request DTOs
| DTO | Usage | Endpoint |
|-----|-------|----------|
| `LoginRequestDTO` | Connexion utilisateur | POST /api/auth/login/ |
| `RegisterRequestDTO` | Inscription utilisateur | POST /api/auth/register/ |
| `RefreshTokenRequestDTO` | Rafraîchir token JWT | POST /api/auth/refresh/ |
| `ChangePasswordRequestDTO` | Changer mot de passe | POST /api/users/change-password/ |
| `UpdateUserRequestDTO` | Modifier profil | PATCH /api/users/me/ |

### Response DTOs
| DTO | Usage | Endpoint |
|-----|-------|----------|
| `LoginResponseDTO` | Réponse login (tokens + user) | POST /api/auth/login/ |
| `RegisterResponseDTO` | Réponse inscription | POST /api/auth/register/ |
| `RefreshTokenResponseDTO` | Nouveau access token | POST /api/auth/refresh/ |
| `UserResponseDTO` | Détails utilisateur | GET /api/users/{id}/ |
| `UserListResponseDTO` | Liste utilisateurs | GET /api/users/ |

---

## 💼 Offer DTOs (`offer/serializers.py`)

### Request DTOs
| DTO | Usage | Endpoint |
|-----|-------|----------|
| `CreateOfferRequestDTO` | Créer offre | POST /api/offers/ |
| `UpdateOfferRequestDTO` | Modifier offre | PATCH/PUT /api/offers/{id}/ |

### Response DTOs
| DTO | Usage | Endpoint |
|-----|-------|----------|
| `OfferResponseDTO` | Détails offre complets | GET /api/offers/{id}/ |
| `OfferListResponseDTO` | Liste offres (allégé) | GET /api/offers/ |
| `OfferSummaryDTO` | Résumé ultra-léger | GET /api/offers/search/ |

---

## 🔄 Aliases (Backward Compatibility)

Pour compatibilité avec ancien code:

```python
# Authentication
AuthenticationSerializer = LoginRequestDTO
LoginSerializer = LoginRequestDTO
RegisterSerializer = RegisterRequestDTO
UserSerializer = UserResponseDTO

# Offers
OfferSerializer = OfferResponseDTO
```

---

## 📦 Import rapide

```python
# Authentication
from authentication.serializers import (
    # Auth
    LoginRequestDTO,
    LoginResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO,
    RefreshTokenRequestDTO,
    RefreshTokenResponseDTO,
    
    # Users
    UserResponseDTO,
    UserListResponseDTO,
    UpdateUserRequestDTO,
    ChangePasswordRequestDTO,
)

# Offers
from offer.serializers import (
    CreateOfferRequestDTO,
    UpdateOfferRequestDTO,
    OfferResponseDTO,
    OfferListResponseDTO,
    OfferSummaryDTO,
)
```

---

## 🎯 Correspondance Endpoint → DTO

### Authentication Endpoints

| Méthode | Endpoint | Request DTO | Response DTO |
|---------|----------|-------------|--------------|
| POST | `/api/auth/login/` | `LoginRequestDTO` | `LoginResponseDTO` |
| POST | `/api/auth/register/` | `RegisterRequestDTO` | `RegisterResponseDTO` |
| POST | `/api/auth/refresh/` | `RefreshTokenRequestDTO` | `RefreshTokenResponseDTO` |
| POST | `/api/auth/logout/` | - | - |

### User Endpoints

| Méthode | Endpoint | Request DTO | Response DTO |
|---------|----------|-------------|--------------|
| GET | `/api/users/me/` | - | `UserResponseDTO` |
| PATCH | `/api/users/me/` | `UpdateUserRequestDTO` | `UserResponseDTO` |
| POST | `/api/users/change-password/` | `ChangePasswordRequestDTO` | - |
| GET | `/api/users/` | - | `UserListResponseDTO` (many) |
| GET | `/api/users/{id}/` | - | `UserResponseDTO` |

### Offer Endpoints

| Méthode | Endpoint | Request DTO | Response DTO |
|---------|----------|-------------|--------------|
| POST | `/api/offers/` | `CreateOfferRequestDTO` | `OfferResponseDTO` |
| GET | `/api/offers/` | - | `OfferListResponseDTO` (many) |
| GET | `/api/offers/{id}/` | - | `OfferResponseDTO` |
| PATCH | `/api/offers/{id}/` | `UpdateOfferRequestDTO` | `OfferResponseDTO` |
| PUT | `/api/offers/{id}/` | `UpdateOfferRequestDTO` | `OfferResponseDTO` |
| DELETE | `/api/offers/{id}/` | - | - |
| GET | `/api/offers/search/` | - | `OfferSummaryDTO` (many) |

---

## ✅ Validations par DTO

### LoginRequestDTO
- ✅ Email requis et format valide
- ✅ Password requis
- ✅ Utilisateur existe
- ✅ Compte actif

### RegisterRequestDTO
- ✅ Email unique
- ✅ Password min 8 caractères
- ✅ Passwords correspondent
- ✅ Role valide (recruteur/chercheur)
- ✅ Company_name requis si recruteur

### CreateOfferRequestDTO
- ✅ Titre non vide
- ✅ Responsibilities = liste non vide
- ✅ Requirements = liste non vide
- ✅ MinSalary < MaxSalary
- ✅ Type parmi valeurs autorisées
- ✅ Experience level valide

### UpdateUserRequestDTO
- ✅ Company_name non vide pour recruteur

### ChangePasswordRequestDTO
- ✅ Old password correct
- ✅ New password min 8 caractères
- ✅ Passwords correspondent
