from django.urls import path
from .views import *

app_name = "usuarios"
urlpatterns = [
    path('', ListadoUsuario.as_view()),
    path('<int:pk>', DetalleUsuario.as_view()),
    path('Grupos/', ListadoGrupos.as_view()),
    path('UsuariosGrupos/', Listado_UsuariosPorGrupos.as_view()),
]
