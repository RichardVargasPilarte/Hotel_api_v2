from django.urls import path
from .views import ListadoCliente, DetalleCliente

app_name = 'clientes'

urlpatterns = [
    path('', ListadoCliente.as_view()),
    path('<int:pk>', DetalleCliente.as_view())
]