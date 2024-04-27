from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Alojamiento
from .serializers import alojamientoSerializer

from Hotel_api.http_responses import HTTPResponse, HTTPResponseText

from django.core.paginator import Paginator

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Alojamiento.objects.all()

class ListadoAlojamiento(APIView, ClassQuery):

    # autenticacion
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        try:

            # Se captura el parametro a buscar
            query = request.query_params.get('q')
            
            if query:
                # Busqueda se realiza en base al nombre y que no este eliminado
                alojamientos = Alojamiento.objects.filter(
                    eliminado="NO", nombre__icontains=query).order_by('id')
            else:
                # En caso de no coincidir la busquedad se lista los alojamientos
                alojamientos = Alojamiento.objects.filter(
                    eliminado="NO").order_by('id')
            
            # Paginar los resultados
            paginator = Paginator(alojamientos, 10)  # 10 elementos por página
            page_number = request.query_params.get('page')
            page_obj = paginator.get_page(page_number)

            serializer = alojamientoSerializer(page_obj, many=True)

            # Obtener el número total de registros y calcular el número total de páginas
            total_registros = paginator.count
            total_paginas = paginator.num_pages
            
            # Obtener información sobre la página actual y las páginas disponibles
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

            # return Response(dict(data=serializer.data, code=HTTPResponse.OK()))
        except:
            response = 'Registros no encontrados'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def post(self, request):
        try:
            alojamiento = request.data.get('alojamiento')
            print(alojamiento)
            serializer = alojamientoSerializer(data=alojamiento)
            if serializer.is_valid(raise_exception=True):
                alojamiento_saved = serializer.save()
            return Response(dict(message=f"Alojamiento: '{alojamiento_saved.nombre}' creada satisfactoriamente".format(), code=HTTPResponse.CREATED()))
        except:
            response = 'Registro no creado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))


class DetalleAlojamiento(APIView, ClassQuery):

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, pk):
        try:
            alojamientos = Alojamiento.objects.get(id=pk)
            serializer = alojamientoSerializer(alojamientos)
            return Response(dict(alojamientos=serializer.data, code=HTTPResponse.OK()))
        except:
            response = 'Registro no encontrado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def put(self, request, pk):
        try:
            saved_alojamientos = get_object_or_404(
                Alojamiento.objects.all(), id=pk)
            alojamientos = request.data.get('alojamientos')
            print('llego el alojamiento: ', alojamientos)
            serializer = alojamientoSerializer(
                instance=saved_alojamientos, data=alojamientos, partial=True)
            if serializer.is_valid(raise_exception=True):
                alojamiento_saved = serializer.save()
            return Response(dict(message=f'Alojamiento [{alojamiento_saved.nombre}] actualizado correctamente', code=HTTPResponse.OK()))
        except:
            response = 'Hubo un error al actializar el registro'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def delete(self, request, pk):
        try:
            response = HTTPResponseText.OK()
            alojamientos = get_object_or_404(Alojamiento.objects.all(), id=pk)
            alojamientos.eliminado = 'SI'
            alojamiento_saved = alojamientos.save()
            return Response(dict(message=f'Alojamiento con id `[{pk}]` fue eliminado.'), status=HTTPResponse.NO_CONTENT())
        except:
            response = 'Registro no eliminado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))