from django.urls import path
from .views import listado_cliente, detalle_cliente

app_name = 'clientes'

urlpatterns = [
    path('', listado_cliente.as_view()),
    path('<int:pk>', detalle_cliente.as_view())
]