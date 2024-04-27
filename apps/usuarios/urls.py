from django.urls import path
from .views import *

app_name = "usuarios"
urlpatterns = [
    path('', ListadoUsuario.as_view()),
    path('<int:pk>', DetalleUsuario.as_view()),
    path('Grupos/', ListadoGrupos.as_view()),
    path('UsuariosGrupos/', ListadoUsuariosPorGrupos.as_view()),
    path('Permisos/', ListadoPermisos.as_view()),
    path('CambiarContrasena/<int:pk>', CambioContrasena.as_view()),
    path('EnviarCorreos/', EnviarCorreos.as_view())
]
