from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Alojamiento
from .serializers import alojamientoSerializer

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Alojamiento.objects.all()

class listado_alojamiento(APIView, ClassQuery):

    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        try:
            alojamientos = Alojamiento.objects.filter(
                eliminado="NO").order_by('id')
            serializer = alojamientoSerializer(alojamientos, many=True)
            return Response(dict(alojamiento=serializer.data))
        except:
            return Response(dict(alojamientos=[], detail="not found"))

    def post(self, request):
        alojamiento = request.data.get('alojamiento')
        print(alojamiento)
        serializer = alojamientoSerializer(data=alojamiento)
        if serializer.is_valid(raise_exception=True):
            alojamiento_saved = serializer.save()
        return Response(dict(success=f"Alojamiento: '{alojamiento_saved.nombre}' creada satisfactoriamente".format()))

class detalle_alojamiento(APIView, ClassQuery):

    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (DjangoModelPermissions,)

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, pk):
        try:
            alojamientos = Alojamiento.objects.get(id=pk)
            serializer = alojamientoSerializer(alojamientos)
            return Response(dict(alojamientos=serializer.data))
        except:
            return Response(dict(alojamientos=[], detail="not found"))

    def put(self, request, pk):
        saved_alojamientos = get_object_or_404(
            Alojamiento.objects.all(), id=pk)
        alojamientos = request.data.get('alojamientos')
        print('llego el alojamiento: ', alojamientos)
        serializer = alojamientoSerializer(
            instance=saved_alojamientos, data=alojamientos, partial=True)
        if serializer.is_valid(raise_exception=True):
            alojamiento_saved = serializer.save()
        return Response(dict(success=f'Alojamiento [{alojamiento_saved.nombre}] actualizado correctamente'))

    def delete(self, request, pk):
        alojamientos = get_object_or_404(Alojamiento.objects.all(), id=pk)
        alojamientos.eliminado = 'SI'
        alojamiento_saved = alojamientos.save()
        return Response(dict(message=f'Alojamiento con id `[{pk}]` fue eliminado.'), status=204)
