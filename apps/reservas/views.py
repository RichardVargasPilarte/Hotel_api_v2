from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Reserva
from .serializers import reservaSerializer, reservaSerializerPost

from Hotel_api.http_responses import HTTPResponse, HTTPResponseText
from django.core.paginator import Paginator

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Reserva.objects.all()
    
class ListadoReserva(APIView, ClassQuery):
    
    permissions = [IsAuthenticated]
    permissions = (DjangoModelPermissions)
    
    def get(self, request):
        try:

            query = request.query_params.get('q')

            if query:
                reservaciones = Reserva.objects.filter(eliminado="NO", nombre__icontains=query).order_by('id')
            else:
                reservaciones = Reserva.objects.filter(eliminado="NO").order_by('id')

            paginator = Paginator(reservaciones, 10)
            page_number = request.query_params.get('page')
            page_obj = paginator.get_page(page_number)

            serializer = reservaSerializer(page_obj, many=True)
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
            reservacion = request.data.get('reservacion')
            print(reservacion)
            serializers = reservaSerializerPost(data=reservacion)
            if serializers.is_valid(raise_exception=True):
                reservacion_saved = serializers.save()
            return Response(dict(message=f"Reserva: '{reservacion_saved.id}' creada satisfactoriamente".format(), code=HTTPResponse.CREATED()))
        except:
            response = 'Registro no creado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))    

class DetalleReserva(APIView, ClassQuery):
    
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions)
    
    def get(self ,pk):
        try:
            reservaciones = Reserva.objects.get(id=pk)
            serializer = reservaSerializerPost(reservaciones)
            return Response(dict(reservaciones=serializer.data, code=HTTPResponse.OK()))
        except:
            return Response(dict(data=[], detail="not found", code=HTTPResponse.NOT_FOUND()))
        
    def put(self, request, pk):
        try:
            saved_reservaciones = get_object_or_404(Reserva.objects.all(), id=pk)
            reservaciones = request.data.get('reservaciones')
            print('llego la reservacion: ', reservaciones)
            serializer = reservaSerializerPost(instance=saved_reservaciones, data=reservaciones, partial=True)
            if serializer.is_valid(raise_exception=True):
                reservacion_saved = serializer.save()
            return Response(dict(message=f'Reservacion [{reservacion_saved.nombre}] actualizada correctamente', code=HTTPResponse.OK()))
        except:
            response = 'Hubo un error al actializar el registro'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))
    def delete(self, pk):
        try:
            response = HTTPResponseText.OK()
            reservaciones = get_object_or_404(Reserva.objects.all(), id=pk)
            reservaciones.eliminado = 'SI'
            reservacion_saved = reservaciones.save()
            return Response(dict(message=f"Reservacion con id `{pk}` fue eliminada"), status=HTTPResponse.NO_CONTENT())
        except:
            response = 'Registro no eliminado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))