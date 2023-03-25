from django.urls import path
from .views import ListadoHabitacion, DetalleHabitacion

app_name = "habitaciones"

urlpatterns = [
    path('', ListadoHabitacion.as_view()),
    path('<int:pk>', DetalleHabitacion.as_view())
]