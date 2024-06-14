import datetime
from django.db import models
from rest_framework import serializers
from .models import Usuario
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q

class usuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('id',
                    'first_name',
                    'last_name',
                    'password',
                    'username',
                    'email',
                    'direccion',
                    'telefono',
                    'eliminado',
                    'groups'
                )
        depth = 1


class gruposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
                    'id',
                    'name'
                )

class gruposPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['permissions']


class usuariosSerializerPOST(serializers.ModelSerializer):

    def create(self, validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        act_usuario = super().update(instance, validated_data)
        act_usuario.set_password(validated_data['password'])
        act_usuario.save()
        return act_usuario

    class Meta:
        model = Usuario
        fields = (  'id',
                    'first_name',
                    'last_name',
                    'password',
                    'username',
                    'email',
                    'direccion',
                    'telefono',
                    'eliminado',
                    'groups',
                )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # grupos = gruposPermissionSerializer(user.groups,  many=True)
        # grupos = gruposSerializer(user.groups,  many=True)
        # grupos = grupos.data[0]['name']
        # grupo = list(user.groups.values_list('name')) # primera opcion: método devuelve un QuerySet que contiene tuplas
        groups = list(user.groups.values('id')) # segunda opcion: método devuelve una lista de diccionarios
        permissions = Permission.objects.filter(Q(user=user) | Q(group__user=user)).all()
        # Add custom claims
        token['name'] = user.username
        token['groups'] = groups
        token['permissions'] = [p.id for p in permissions]
        print(token['name'])
        print(groups)
        # print(permissions)
        print(token)
        return token
    
    # todas las declaraciones que se realxionan al grupo del usuario son las del error
    

class permisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
        

class cambioContraseñaSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)