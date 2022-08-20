from django.urls import path
from .views import *

app_name = "usuarios"
urlpatterns = [
    path('', listado_usuario.as_view()),
    path('<int:pk>', detalle_usuario.as_view()),
    path('Grupos/', listado_grupos.as_view()),
    path('UsuariosGrupos', listado_UsuariosPorGrupos.as_view()),
]
