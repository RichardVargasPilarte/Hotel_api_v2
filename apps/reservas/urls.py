from django.urls import path
from .views import listado_reserva, detalle_reserva

app_name = 'reservaciones'

urlpatterns = [
    path('', listado_reserva.as_view()),
    path('<int:pk>', detalle_reserva.as_view()),
]