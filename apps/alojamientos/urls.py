from django.urls import path
from .views import ListadoAlojamiento, detalle_alojamiento

app_name = 'alojamientos'

urlpatterns = [
    path('', ListadoAlojamiento.as_view()),
    path('<int:pk>', detalle_alojamiento.as_view())
]