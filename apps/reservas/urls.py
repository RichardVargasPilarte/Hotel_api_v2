from django.urls import path
from .views import ListadoReserva, DetalleReserva

app_name = 'reservaciones'

urlpatterns = [
    path('', ListadoReserva.as_view()),
    path('<int:pk>', DetalleReserva.as_view()),
]