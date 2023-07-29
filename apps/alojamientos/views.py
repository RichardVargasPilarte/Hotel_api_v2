from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Alojamiento
from .serializers import alojamientoSerializer

from Hotel_api.http_responses import HTTPResponse, HTTPResponseText

# Create your views here.
class ClassQuery():
    def get_queryset(self):
        return Alojamiento.objects.all()

class ListadoAlojamiento(APIView, ClassQuery):

    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request):
        try:
            # status_code = 200
            # response = HTTPResponse.get_message(status_code)
            alojamientos = Alojamiento.objects.filter(
                eliminado="NO").order_by('id')
            serializer = alojamientoSerializer(alojamientos, many=True)
            print(HTTPResponse.OK())
            return Response(dict(data=serializer.data, code=HTTPResponse.OK()))
        except:
            # status_code = 404
            response = 'Registros no encontrados'  # Default custom message for other errors
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))
            # return Response(dict(data=[], detail="not found", code=status_code))

    def post(self, request):
        try:
            # status_code = 201
            # response = HTTPResponse.get_message(status_code)
            alojamiento = request.data.get('alojamiento')
            print(alojamiento)
            serializer = alojamientoSerializer(data=alojamiento)
            if serializer.is_valid(raise_exception=True):
                alojamiento_saved = serializer.save()
            return Response(dict(message=f"Alojamiento: '{alojamiento_saved.nombre}' creada satisfactoriamente".format(), code=HTTPResponse.CREATED()))
        except:
            # status_code = 404
            response = 'Registro no creado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))


class DetalleAlojamiento(APIView, ClassQuery):

    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (DjangoModelPermissions,)

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, pk):
        try:
            # status_code = 200
            # response = HTTPResponse.get_message(status_code)
            alojamientos = Alojamiento.objects.get(id=pk)
            serializer = alojamientoSerializer(alojamientos)
            return Response(dict(alojamientos=serializer.data, code=HTTPResponse.OK()))
        except:
            # status_code = 404
            response = 'Registro no encontrado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def put(self, request, pk):
        try:
            # status_code = 200
            # response = HTTPResponse.get_message(status_code)
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
            # status_code = 404
            response = 'Hubo un error al actializar el registro'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))

    def delete(self, request, pk):
        try:
            # status_code = 204
            response = HTTPResponseText.OK()
            alojamientos = get_object_or_404(Alojamiento.objects.all(), id=pk)
            alojamientos.eliminado = 'SI'
            alojamiento_saved = alojamientos.save()
            return Response(dict(message=f'Alojamiento con id `[{pk}]` fue eliminado.'), status=HTTPResponse.NO_CONTENT())
            
        except:
            # status_code = 404
            response = 'Registro no eliminado'
            return Response(dict(data=[], detail=response, code=HTTPResponse.NOT_FOUND()))