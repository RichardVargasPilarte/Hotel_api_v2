from django.urls import path
from .views import ListadoAlojamiento, DetalleAlojamiento

app_name = 'alojamientos'

urlpatterns = [
    path('', ListadoAlojamiento.as_view()),
    path('<int:pk>', DetalleAlojamiento.as_view())
]