from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Alojamiento
from .serializers import alojamientoSerializer

from Hotel_api.http_responses import HTTPResponse

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
            status_code = 200
            response = HTTPResponse.get_message(status_code)
            alojamientos = Alojamiento.objects.filter(
                eliminado="NO").order_by('id')
            serializer = alojamientoSerializer(alojamientos, many=True)
            return Response(dict(data=serializer.data, code=status_code))
        except:
            status_code = 404
            response = 'Registros no encontrados'  # Default custom message for other errors

            # Handle specific codes differently
            if specific_condition_1:
                status_code = 400
                response = HTTPResponse.get_message(status_code)
            elif specific_condition_2:
                status_code = 401
                response = HTTPResponse.get_message(status_code)
            else:
                status_code = 500
                response = HTTPResponse.get_message(status_code)

            return Response(dict(data=[], detail=response, code=status_code))
            # return Response(dict(data=[], detail="not found", code=status_code))

    def post(self, request):
        try:
            status_code = 201
            response = HTTPResponse.get_message(status_code)
            alojamiento = request.data.get('alojamiento')
            print(alojamiento)
            serializer = alojamientoSerializer(data=alojamiento)
            if serializer.is_valid(raise_exception=True):
                alojamiento_saved = serializer.save()
            return Response(dict(message=f"Alojamiento: '{alojamiento_saved.nombre}' creada satisfactoriamente".format(), code=status_code))
        except:
            status_code = 404
            response = 'Registro no creado'
            
            # Handle specific codes differently
            if specific_condition_1:
                status_code = 400
                response = HTTPResponse.get_message(status_code)
            elif specific_condition_2:
                status_code = 401
                response = HTTPResponse.get_message(status_code)
            else:
                status_code = 500
                response = HTTPResponse.get_message(status_code)

            return Response(dict(data=[], detail=response, code=status_code))


class DetalleAlojamiento(APIView, ClassQuery):

    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (DjangoModelPermissions,)

    permission_classes = [IsAuthenticated]
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, pk):
        try:
            status_code = 200
            response = HTTPResponse.get_message(status_code)
            alojamientos = Alojamiento.objects.get(id=pk)
            serializer = alojamientoSerializer(alojamientos)
            return Response(dict(alojamientos=serializer.data, code=status_code))
        except:
            status_code = 404
            response = 'Registro no encontrado'
            
            # Handle specific codes differently
            if specific_condition_1:
                status_code = 400
                response = HTTPResponse.get_message(status_code)
            elif specific_condition_2:
                status_code = 401
                response = HTTPResponse.get_message(status_code)
            else:
                status_code = 500
                response = HTTPResponse.get_message(status_code)

            return Response(dict(data=[], detail=response, code=status_code))
            # return Response(dict(alojamientos=[], detail="not found", code=404))

    def put(self, request, pk):
        try:
            status_code = 200
            response = HTTPResponse.get_message(status_code)
            saved_alojamientos = get_object_or_404(
                Alojamiento.objects.all(), id=pk)
            alojamientos = request.data.get('alojamientos')
            print('llego el alojamiento: ', alojamientos)
            serializer = alojamientoSerializer(
                instance=saved_alojamientos, data=alojamientos, partial=True)
            if serializer.is_valid(raise_exception=True):
                alojamiento_saved = serializer.save()
            return Response(dict(message=f'Alojamiento [{alojamiento_saved.nombre}] actualizado correctamente', code=status_code))
    
        except:
            status_code = 404
            response = 'Hubo un error al actializar el registro'
            
            # Handle specific codes differently
            if specific_condition_1:
                status_code = 400
                response = HTTPResponse.get_message(status_code)
            elif specific_condition_2:
                status_code = 401
                response = HTTPResponse.get_message(status_code)
            else:
                status_code = 500
                response = HTTPResponse.get_message(status_code)

            return Response(dict(data=[], detail=response, code=status_code))


    def delete(self, request, pk):
        try:
            status_code = 204
            response = HTTPResponse.get_message(status_code)
            alojamientos = get_object_or_404(Alojamiento.objects.all(), id=pk)
            alojamientos.eliminado = 'SI'
            alojamiento_saved = alojamientos.save()
            return Response(dict(message=f'Alojamiento con id `[{pk}]` fue eliminado.'), status=204)
            
        except:
            status_code = 404
            response = 'Registro no eliminado'

            if specific_condition_1:
                status_code = 400
                response = HTTPResponse.get_message(status_code)
            elif specific_condition_2:
                status_code = 401
                response = HTTPResponse.get_message(status_code)
            else:
                status_code = 500
                response = HTTPResponse.get_message(status_code)
                
            return Response(dict(data=[], detail=response, code=status_code))