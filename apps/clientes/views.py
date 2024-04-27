from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cliente
from .serializers import clienteSerializer

from Hotel_api.http_responses import HTTPResponse, HTTPResponseText
from django.core.paginator import Paginator

# Create your views here.


class ClassQuery:
    def get_queryset(self):
        return Cliente.objects.all()


class ListadoCliente(APIView, ClassQuery):
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        try:
            query = request.query_params.get('q')

            if query:
                clientes = Cliente.objects.filter(eliminado="NO", nombre__icontains=query).order_by('id')
            else:
                clientes = Cliente.objects.filter(eliminado="NO").order_by('id')

            paginator = Paginator(clientes, 10)
            page_number = request.query_params.get('page')
            page_obj = paginator.get_page(page_number)

            serializer = clienteSerializer(page_obj, many=True)

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
        
            # return Response(dict(data=serializer.data, code=200))
        except:
            response = 'Registros no encontrados'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def post(self, request):
        try:
            cliente = request.data.get("cliente")
            print(cliente)
            serializer = clienteSerializer(data=cliente)
            if serializer.is_valid(raise_exception=True):
                cliente_saved = serializer.save()
            return Response(
                dict(
                    message=f"Cliente: '{cliente_saved.nombre}' creado satisfactoriamente".format(),
                    code=HTTPResponse.CREATED()
                )
            )
        except:
            response = 'Registro no creado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

class DetalleCliente(APIView, ClassQuery):

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, pk):
        try:
            clientes = Cliente.objects.get(id=pk)
            serializer = clienteSerializer(clientes)
            return Response(dict(clientes=serializer.data, code=HTTPResponse.OK()))
        except:
            return Response(dict(clientes=[], error="not found", code=HTTPResponse.NOT_FOUND()))

    def put(self, request, pk):
        try:
            saved_clientes = get_object_or_404(Cliente.objects.all(), id=pk)
            clientes = request.data.get("clientes")
            print("llego el cliente: ", clientes)
            serializer = clienteSerializer(
                instance=saved_clientes, data=clientes, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                cliente_saved = serializer.save()
            return Response(
                dict(
                    message=f"Cliente [{cliente_saved.nombre}] actualizado correctamente",
                    code=HTTPResponse.OK()
                )
            )
        except:
            response = 'Hubo un error al actializar el registro'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def delete(self, request, pk):
        try:
            response = HTTPResponseText.OK()
            clientes = get_object_or_404(Cliente.objects.all(), id=pk)
            clientes.eliminado = "SI"
            cliente_saved = clientes.save()
            return Response(
                dict(message=f"Cliente con id `[{pk}]` fue eliminado."), status=HTTPResponse.NO_CONTENT()
            )
        except:
            response = 'Registro no eliminado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))