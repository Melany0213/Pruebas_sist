from rest_framework import viewsets
from .serializer import CertificationSerializer, EstudianteSerializer, Hago_ConstarSerializer, ProfesorSerializer, SolicitudSerializer, ActaSerializer, JuradoSerializer, FolioSerializer
from .models import Certification, Estudiante, Hago_Constar, Profesor, Solicitud, Acta, Jurado, Folio
#from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EstudianteView(viewsets.ModelViewSet):
	serializer_class = EstudianteSerializer
	queryset = Estudiante.objects.all()
	#permission_classes = [IsAuthenticated]

class ProfesorView(viewsets.ModelViewSet):
	serializer_class = ProfesorSerializer
	queryset = Profesor.objects.all()
	#permission_classes = [IsAuthenticated]

class CertificationView(viewsets.ModelViewSet):
	serializer_class = CertificationSerializer
	queryset = Certification.objects.all()
	# permission_classes = [IsAuthenticated]

class ActaView(viewsets.ModelViewSet):
	serializer_class = ActaSerializer
	queryset = Acta.objects.all()
	# permission_classes = [IsAuthenticated]
class SolicitudView(viewsets.ModelViewSet):
	serializer_class = SolicitudSerializer
	queryset = Solicitud.objects.all()
	# permission_classes = [IsAuthenticated]

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
