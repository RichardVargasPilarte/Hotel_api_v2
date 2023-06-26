from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Reserva
from .serializers import reservaSerializer, reservaSerializerPost

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Reserva.objects.all()
    
class ListadoReserva(APIView, ClassQuery):
    
    permissions = [IsAuthenticated]
    permissions = (DjangoModelPermissions)
    
    def get(self, request):
        try:
            reservaciones = Reserva.objects.filter(eliminado="NO").order_by('id')
            serializers = reservaSerializer(reservaciones, many=True)
            return Response(dict(data=serializers.data, code=200))
        except:
            return Response(dict(data=[], detail="not found", code=404))
        
    def post(self, request):
        reservacion = request.data.get('reservacion')
        print(reservacion)
        serializers = reservaSerializerPost(data=reservacion)
        if serializers.is_valid(raise_exception=True):
            reservacion_saved = serializers.save()
        return Response(dict(message=f"Reserva: '{reservacion_saved.id}' creada satisfactoriamente".format(), code=201))
    

class DetalleReserva(APIView, ClassQuery):
    
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions)
    
    def get(self ,pk):
        try:
            reservaciones = Reserva.objects.get(id=pk)
            serializer = reservaSerializerPost(reservaciones)
            return Response(dict(reservaciones=serializer.data, code=200))
        except:
            return Response(dict(reservaciones=[], detail="not found", code=404))
        
    def put(self, request, pk):
        saved_reservaciones = get_object_or_404(Reserva.objects.all(), id=pk)
        reservaciones = request.data.get('reservaciones')
        print('llego la reservacion: ', reservaciones)
        serializer = reservaSerializerPost(instance=saved_reservaciones, data=reservaciones, partial=True)
        if serializer.is_valid(raise_exception=True):
            reservacion_saved = serializer.save()
        return Response(dict(message=f'Reservacion [{reservacion_saved.nombre}] actualizada correctamente', code=200))
    
    def delete(self, pk):
        reservaciones = get_object_or_404(Reserva.objects.all(), id=pk)
        reservaciones.eliminado = 'SI'
        reservacion_saved = reservaciones.save()
        return Response(dict(message=f"Reservacion con id `{pk}` fue eliminada"), status=204)