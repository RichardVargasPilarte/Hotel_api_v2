from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cliente
from .serializers import clienteSerializer

# Create your views here.


class ClassQuery:
    def get_queryset(self):
        return Cliente.objects.all()


class ListadoCliente(APIView, ClassQuery):
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        try:
            clientes = Cliente.objects.filter(eliminado="NO").order_by("id")
            serializer = clienteSerializer(clientes, many=True)
            return Response(dict(data=serializer.data, code=200))
        except:
            return Response(dict(data=[], error="not found", code=404))

    def post(self, request):
        cliente = request.data.get("cliente")
        print(cliente)
        serializer = clienteSerializer(data=cliente)
        if serializer.is_valid(raise_exception=True):
            cliente_saved = serializer.save()
        return Response(
            dict(
                message=f"Cliente: '{cliente_saved.nombre}' creado satisfactoriamente".format(),
                code=201,
            )
        )


class DetalleCliente(APIView, ClassQuery):

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, pk):
        try:
            clientes = Cliente.objects.get(id=pk)
            serializer = clienteSerializer(clientes)
            return Response(dict(clientes=serializer.data, code=200))
        except:
            return Response(dict(clientes=[], error="not found", code=404))

    def put(self, request, pk):
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
                code=200,
            )
        )

    def delete(self, request, pk):
        clientes = get_object_or_404(Cliente.objects.all(), id=pk)
        clientes.eliminado = "SI"
        cliente_saved = clientes.save()
        return Response(
            dict(message=f"Cliente con id `[{pk}]` fue eliminado."), code=204
        )
