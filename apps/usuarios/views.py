from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario, Group
from .serializers import MyTokenObtainPairSerializer, gruposPermissionSerializer, usuariosSerializer, gruposSerializer, usuariosSerializerPOST, permisosSerializer, cambioContraseñaSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from django.db.models import Q

from rest_framework import generics

from utils.send_email_sendgrid import send_email

from django.core.mail import send_mail
from django.conf import settings

class ClassQuery():
    def get_queryset(self):
        return Usuario.objects.all()

class ListadoUsuario(APIView, ClassQuery):
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)
    
    def get(self, request):
        try:
            usuarios = Usuario.objects.filter(eliminado="NO",id__gte=2).order_by('id')
            serializer = usuariosSerializer(usuarios, many=True)
            return Response(dict(data=serializer.data, code=200))
        except:
            return Response(dict(data=[], detail="not found", code=404))

    def post(self, request):
        usuario = request.data.get('usuario')
        grupo = usuario.pop('groups')
        print(grupo)
        serializer = usuariosSerializerPOST(data=usuario)
        if serializer.is_valid(raise_exception=True):
            usuario_saved = serializer.save()
        usuario_saved.groups.add(grupo)
        return Response(dict(message=f"Usuario: '{usuario_saved.username}' creado satisfactoriamente".format(), code=201))

class DetalleUsuario(APIView, ClassQuery):
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)
    
    def get(self, request, pk):
        try:

            usuario = Usuario.objects.get(id=pk)
            print(usuario)
            serializer = usuariosSerializer(usuario)
            return Response(dict(usuarios=serializer.data, code=200))
        except:
            return Response(dict(usuarios=[], detail="not found", code=404))

    def put(self, request, pk):
        saved_usuario = get_object_or_404(
            Usuario.objects.all(), id=pk)
        usuario = request.data.get('usuario')
        print('llego el usuario: ', usuario)
        serializer = usuariosSerializerPOST(
            instance=saved_usuario, data=usuario, partial=True)
        if serializer.is_valid(raise_exception=True):
            usuario_saved = serializer.save()
        return Response(dict(message=f"Usuario '{usuario_saved.username}' actualizado correctamente", code=200))

    def delete(self, request, pk):
        usuario = get_object_or_404(Usuario.objects.all(), id=pk)
        usuario.eliminado = 'SI'
        usuario_saved = usuario.save()
        return Response(dict(message=f"Usuario con id `{pk}` fue eliminado."), status=status.HTTP_204_NO_CONTENT)
    
class ListadoGrupos(APIView, ClassQuery):
    def get(self, request):
        try:
            # Listo los grupos con sus permisos asignados
            grupos = Group.objects.all().order_by('id')
            serializer = gruposSerializer(grupos, many=True)
            return Response(dict(grupos=serializer.data))
        except:
                return Response(dict(grupos=[], detail="not found"))

class Listado_UsuariosPorGrupos(APIView, ClassQuery):
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
        grupo_permisos = Usuario.objects.filter(
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

class ClassQueryPermissions():
    def get_queryset(self):
        return Permission.objects.all()
    
class ListadoPermisos(APIView, ClassQueryPermissions):
    
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)
    
    def get(self, request):
        # try:
            # Listo los grupos con sus permisos asignados
            # permisos = Permission.objects.all().order_by('id')
        permisos = Permission.objects.filter(Q(user=request.user) | Q(group__user=request.user)).all()
        serializer = permisosSerializer(permisos, many=True)
        return Response(dict(permisos=serializer.data, userPermission=self.request.user.get_user_permissions()))
        # except:
                # return Response(dict(permisos=[], detail="not found"))
                

class CambioContrasena(generics.UpdateAPIView):
    
    serializer_class = cambioContraseñaSerializer
    model = Usuario
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, pk):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            
            if self.object.check_password(serializer.data.get("new_password")) & self.object.check_password(serializer.data.get("old_password")):
                return Response({"new_password": ["La nueva contraseña no debe coincidir con la antigua contrasena"]}, status=status.HTTP_400_BAD_REQUEST)
            
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Contraseña incorrecta"]}, status=status.HTTP_400_BAD_REQUEST)
            

            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Contraseña actualizada correctamente',
                'data': []
            }
            
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EnviarCorreos(APIView):
    
    # Prueba con SendGrid
    
    # def post(self, request, *args, **kwargs):
    #     subject = request.data.get('subject')
    #     message = request.data.get('message')
    #     id = request.data.get('id')
        
    #     if not subject or not message or not id:
    #         return Response({'error': 'Datos Incompletos'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         user = Usuario.objects.get(id=id)
    #     except Usuario.DoesNotExist:
    #         return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    #     user_email = user.email
        
        # response_status = send_email(subject, message, user_email )
        # if response_status == status.HTTP_202_ACCEPTED:
        #     return Response({'message': 'Correo electrónico enviado correctamente'})
        # else:
        #     return Response({'error': 'No se pudo enviar el correo electrónico'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    # Prueba con Gmail 
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        subject = 'Hola, Usuario del sistema'
        message = 'Este correo es de prueba y procede desde gmail.'
        email= request.data.get('email')
        
        try:
            user = Usuario.objects.get(email=email)
            recipient_email = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
            
            return Response({'message': 'Correo electrónico enviado correctamente'})
        
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': 'No se pudo enviar el correo electrónico'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# password reset
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        'token':reset_password_token.key
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Restablecimiento de contraseña para {title}".format(title="Sistema Hotel"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
