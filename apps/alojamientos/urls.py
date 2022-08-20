from django.urls import path
from .views import listado_alojamiento, detalle_alojamiento

app_name = 'alojamientos'

urlpatterns = [
    path('', listado_alojamiento.as_view()),
    path('<int:pk>', detalle_alojamiento.as_view())
]