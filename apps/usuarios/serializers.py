import datetime
from django.db import models
from rest_framework import serializers
from .models import Usuarios, Group
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class usuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuarios
        fields = ('id',
                    'first_name',
                    'last_name',
                    'password',
                    'username',
                    'email',
                    'direccion',
                    'estado',
                    'telefono',
                    'eliminado',
                    'groups'
                )
        depth = 1


class gruposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class gruposPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['permissions']


class usuariosSerializerPOST(serializers.ModelSerializer):

    def create(self, validated_data):
        usuario = Usuarios(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        act_usuario = super().update(instance, validated_data)
        act_usuario.set_password(validated_data['password'])
        act_usuario.save()
        return act_usuario

    class Meta:
        model = Usuarios
        fields = (  'id',
                    'first_name',
                    'last_name',
                    'password',
                    'username',
                    'email',
                    'direccion',
                    'estado',
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
        grupo = list(user.groups.values('name')) # segunda opcion: método devuelve una lista de diccionarios
        # Add custom claims
        token['name'] = user.username
        token['groups'] = grupo
        print(token['name'])
        print(grupo)
        print(token)
        return token
    
    # todas las declaraciones que se realxionan al grupo del usuario son las del error
    
