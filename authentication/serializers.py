from dj_rest_auth.registration.serializers import RegisterSerializer as DjRestAuthRegisterSerializer
from rest_framework import serializers

from company.models import Company
from user_role.models import Role

from .models import User


class RegisterSerializer(DjRestAuthRegisterSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        role = attrs.get('role')
        company = attrs.get('company')

        if role and role.code == 'recruteur' and company is None:
            raise serializers.ValidationError(
                {'company': "L'entreprise est obligatoire pour un recruteur."}
            )

        return attrs

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['role'] = self.validated_data.get('role')
        data['company'] = self.validated_data.get('company')
        return data

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.role = self.validated_data.get('role')
        user.company = self.validated_data.get('company')
        user.save(update_fields=['first_name', 'last_name', 'role', 'company'])

    class Meta:
        model = User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'company']