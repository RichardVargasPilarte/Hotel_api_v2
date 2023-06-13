from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Habitacion
from .serializers import habitacionSerializer, habitacionSerializerPOST

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Habitacion.objects.all()

class ListadoHabitacion(APIView, ClassQuery):

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)
    
    def get(self, request):
        try:
            habitaciones = Habitacion.objects.filter(eliminado="NO").order_by('id')
            serializer = habitacionSerializer(habitaciones, many=True)
            return Response(dict(data=serializer.data, code=200))
        except:
            return Response(dict(data=[], detail="not found", code=404))
    
    def post(self, request):
        habitacion = request.data.get('habitacion')
        print(habitacion)
        serializer = habitacionSerializerPOST(data=habitacion)
        if serializer.is_valid(raise_exception=True):
            habitacion_saved = serializer.save()
        return Response(dict(message=f"Habitacion: '{habitacion_saved.nombre}' creada satisfactoriamente".format(), code=200))


class DetalleHabitacion(APIView, ClassQuery):

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)
    
    def get(self, request, pk):
        try:
            habitaciones = Habitacion.objects.get(id=pk)
            serializer = habitacionSerializerPOST(habitaciones)
            return Response(dict(habitaciones=serializer.data, code=200))
        except:
            return Response(dict(habitaciones=[], detail="not found", code=404))

    def put(self, request, pk):
        saved_habitaciones = get_object_or_404(Habitacion.objects.all(), id=pk)
        habitaciones = request.data.get('habitaciones')
        print('llego la habitacion: ', habitaciones)
        serializer = habitacionSerializerPOST(
            instance=saved_habitaciones, data=habitaciones, partial=True)
        if serializer.is_valid(raise_exception=True):
            habitacion_saved = serializer.save()
        return Response(dict(message=f'Habitacion [{habitacion_saved.nombre}] actualizada correctamente', code=200))

    def delete(self, request, pk):
        habitaciones = get_object_or_404(Habitacion.objects.all(), id=pk)
        habitaciones.eliminado = 'SI'
        habitacion_saved = habitaciones.save()
        return Response(dict(message=f"Habitacion with id `{pk}` fue eliminada."), status=204)
