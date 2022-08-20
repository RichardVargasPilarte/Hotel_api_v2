from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuarios, Group
from .serializers import MyTokenObtainPairSerializer, gruposPermissionSerializer, usuariosSerializer, gruposSerializer, usuariosSerializerPOST
from rest_framework_simplejwt.views import TokenObtainPairView

class Class_query():
    def get_queryset(self):
        return Usuarios.objects.all()

class listado_usuario(APIView, Class_query):
    def get(self, request):
        try:
            usuarios = Usuarios.objects.filter(eliminado="NO").order_by('id')
            serializer = usuariosSerializer(usuarios, many=True)
            return Response(dict(usuario=serializer.data))
        except:
            return Response(dict(usuario=[], detail="not found"))

    def post(self, request):
        usuario = request.data.get('usuario')
        grupo = usuario.pop('tipo_usuario')
        print(grupo)
        serializer = usuariosSerializerPOST(data=usuario)
        if serializer.is_valid(raise_exception=True):
            usuario_saved = serializer.save()
        usuario_saved.groups.add(grupo)
        return Response(dict(success=f"Usuarios: '{usuario_saved.username}' creado satisfactoriamente".format()))

class detalle_usuario(APIView, Class_query):
    def get(self, request, pk):
        try:

            usuario = Usuarios.objects.get(id=pk)
            print(usuario)
            serializer = usuariosSerializer(usuario)
            return Response(dict(usuario=serializer.data))
        except:
            return Response(dict(usuario=[], detail="not found"))

    def put(self, request, pk):
        saved_usuario = get_object_or_404(
            Usuarios.objects.all(), id=pk)
        usuario = request.data.get('usuario')
        print('llego el usuario: ', usuario)
        serializer = usuariosSerializerPOST(
            instance=saved_usuario, data=usuario, partial=True)
        if serializer.is_valid(raise_exception=True):
            usuario_saved = serializer.save()
        return Response(dict(success=f"Usuarios '{usuario_saved.username}' actualizado correctamente"))

    def delete(self, request, pk):
        usuario = get_object_or_404(Usuarios.objects.all(), id=pk)
        usuario.eliminado = 'SI'
        usuario_saved = usuario.save()
        return Response(dict(message=f"Usuario con id `{pk}` fue eliminado."), status=204)
    
class listado_grupos(APIView, Class_query):
    def get(self, request):
        try:
            # Listo los grupos con sus permisos asignados
            grupos = Group.objects.all().order_by('id')
            serializer = gruposSerializer(grupos, many=True)
            return Response(dict(grupos=serializer.data))
        except:
                return Response(dict(grupos=[], detail="not found"))

class listado_UsuariosPorGrupos(APIView, Class_query):
    def get(self, request):
        # ----------------------------------------------------------------
        # Obtengo todos los permisos que posee el usuario actual, mediante dos consultas
        # separadas, una sobre grupos y otra sobre permisos y los resultados se guardan en group_ids
        # ----------------------------------------------------------------
        # group_ids = Group.objects.all().values_list('id', flat=True)
        # group_ids = Permission.objects.filter(group__id__in=group_ids)

        # grupo_permisos captura los resultados de group_ids y despues se muestran
        # grupo_permisos = group_ids
        # ----------------------------------------------------------------

        # muestro los usuarios segun su grupo, pero falta agregar el campo id
        # del grupo en la respuesta
        grupo_permisos = Usuarios.objects.filter(
            groups__name__in=['Administrador', 'Supervisor', 'Común']).order_by('id')
        serializer = usuariosSerializer(grupo_permisos, many=True)
        print(grupo_permisos)
        return Response(dict(usuarios_segun_grupo=serializer.data, detail="not found"))

# class UserLoginViewJWT(jwt_views.ObtainJSONWebToken):
#     user_serializer_class = usuariosSerializer

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)

#         if response.status_code == status.HTTP_200_OK:
#             user = get_user_model().objects.get(
#                 email=request.data[get_user_model().USERNAME_FIELD])
#             serialized_user = self.user_serializer_class(user)
#             response.data.update(serialized_user.data)
#         return response

# def jwt_response_payload_handler(token, user=None, request=None):
#     grupos = gruposPermissionSerializer(user.groups,  many=True)
#     grupos =grupos.data[0]['permissions']
#     return {
#         'token': token,
#         'grupos': grupos
#     }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
