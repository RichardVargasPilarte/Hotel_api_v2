from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Habitacion
from .serializers import habitacionSerializer, habitacionSerializerPOST

from Hotel_api.http_responses import HTTPResponse, HTTPResponseText
from django.core.paginator import Paginator

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Habitacion.objects.all()

class ListadoHabitacion(APIView, ClassQuery):
    
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        try:

            query = request.query_params.get('q')

            if query:
                habitaciones = Habitacion.objects.filter(eliminado="NO", nombre__icontains=query).order_by('id')
            else:
                habitaciones = Habitacion.objects.filter(eliminado="NO").order_by('id')

            paginator = Paginator(habitaciones, 10)
            page_number = request.query_params.get('page')
            page_obj = paginator.get_page(page_number)

            serializer = habitacionSerializer(page_obj, many=True)

            total_registros = paginator.count
            total_paginas = paginator.num_pages

            pagina_actual = page_obj.number
            paginas_disponibles = {
                'anterior': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'siguiente': page_obj.next_page_number() if page_obj.has_next() else None,
            }

            return Response({
                'data': serializer.data,
                'total_registros': total_registros,
                'total_paginas': total_paginas,
                'pagina_actual': pagina_actual,
                'paginas_disponibles': paginas_disponibles,
                'code': HTTPResponse.OK()
            })
        except:
            response = 'Registros no encontrados'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    
    def post(self, request):
        try:
            habitacion = request.data.get('habitacion')
            print(habitacion)
            serializer = habitacionSerializerPOST(data=habitacion)
            if serializer.is_valid(raise_exception=True):
                habitacion_saved = serializer.save()
            return Response(dict(message=f"Habitacion: '{habitacion_saved.nombre}' creada satisfactoriamente".format(), code=HTTPResponse.CREATED()))
        except:
            response = 'Registro no creado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

class DetalleHabitacion(APIView, ClassQuery):

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)
    
    def get(self, request, pk):
        try:
            habitaciones = Habitacion.objects.get(id=pk)
            serializer = habitacionSerializerPOST(habitaciones)
            return Response(dict(habitaciones=serializer.data, code=HTTPResponse.OK()))
        except:
            return Response(dict(habitaciones=[], detail="not found", code=HTTPResponse.NOT_FOUND()))

    def put(self, request, pk):
        try:
            saved_habitaciones = get_object_or_404(Habitacion.objects.all(), id=pk)
            habitaciones = request.data.get('habitaciones')
            print('llego la habitacion: ', habitaciones)
            serializer = habitacionSerializerPOST(
                instance=saved_habitaciones, data=habitaciones, partial=True)
            if serializer.is_valid(raise_exception=True):
                habitacion_saved = serializer.save()
            return Response(dict(message=f'Habitacion [{habitacion_saved.nombre}] actualizada correctamente', code=HTTPResponse.OK()))
        except:
            response = 'Hubo un error al actializar el registro'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))
    def delete(self, request, pk):
        try:
            response = HTTPResponseText.OK()
            habitaciones = get_object_or_404(Habitacion.objects.all(), id=pk)
            habitaciones.eliminado = 'SI'
            habitacion_saved = habitaciones.save()
            return Response(dict(message=f"Habitacion with id `{pk}` fue eliminada."), status=HTTPResponse.NO_CONTENT())
        except:
            response = 'Registro no eliminado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))