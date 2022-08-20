from django.urls import path
from .views import listado_habitacion, detalle_habitacion

app_name = "habitaciones"

urlpatterns = [
    path('', listado_habitacion.as_view()),
    path('<int:pk>', detalle_habitacion.as_view())
]