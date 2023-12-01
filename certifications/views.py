from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import CertificationSerializer, EstudianteSerializer, Hago_ConstarSerializer, ProfesorSerializer, SolicitudSerializer, JuradoSerializer, FolioSerializer, ActaSerializer
from .models import Certification, Estudiante, Hago_Constar, Profesor, Solicitud, Jurado, Folio


class EstudianteView(viewsets.ModelViewSet):
	serializer_class = EstudianteSerializer
	queryset = Estudiante.objects.all()
	# permission_classes = [IsAuthenticated]

class ProfesorView(viewsets.ModelViewSet):
	serializer_class = ProfesorSerializer
	queryset = Profesor.objects.all()
	# permission_classes = [IsAuthenticated]

class CertificationView(viewsets.ModelViewSet):
	serializer_class = CertificationSerializer
	queryset = Certification.objects.all()
	# permission_classes = [IsAuthenticated]

class SolicitudView(viewsets.ModelViewSet):
	serializer_class = SolicitudSerializer
	# queryset = Solicitud.objects.filter(date_has_solicitud=F('estudiante__solicitud__date_has_solicitud'))
	queryset = Solicitud.objects.all()
	# permission_classes = [IsAuthenticated]

	@action(detail=True, methods=['POST'], serializer_class=ActaSerializer)
	def update_acta(self, request, pk=None):
		solicitud = Solicitud.objects.get(pk=pk)
		serializer = ActaSerializer(solicitud, data=request.data, partial=True)
		serializer.is_valid()
		serializer.save()
		return Response(data=serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

class JuradoView(viewsets.ModelViewSet):
	serializer_class = JuradoSerializer
	queryset = Jurado.objects.all()
	# permission_classes = [IsAuthenticated]
class FolioView(viewsets.ModelViewSet):
	serializer_class = FolioSerializer
	queryset = Folio.objects.all()
	# permission_classes = [IsAuthenticated]

class Hago_ConstarView(viewsets.ModelViewSet):
	serializer_class = Hago_ConstarSerializer
	queryset = Hago_Constar.objects.all()
	# permission_classes = [IsAuthenticated]
