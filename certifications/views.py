from rest_framework import viewsets
from .serializer import CertificationsSerializer, EstudianteSerializer, Hago_ConstarSerializer, ProfesorSerializer, SolicitudesSerializer
from .models import Certifications, Estudiante, Hago_Constar, Profesor, Solicitudes


# Create your views here.
class EstudianteView(viewsets.ModelViewSet):
	serializer_class = EstudianteSerializer
	queryset = Estudiante.objects.all()

class ProfesorView(viewsets.ModelViewSet):
	serializer_class = ProfesorSerializer
	queryset = Profesor.objects.all()

class CertificationsView(viewsets.ModelViewSet):
	serializer_class = CertificationsSerializer
	queryset = Certifications.objects.all()

class Hago_ConstarView(viewsets.ModelViewSet):
	serializer_class = Hago_ConstarSerializer
	queryset = Hago_Constar.objects.all()

class SolicitudesView(viewsets.ModelViewSet):
	serializer_class = SolicitudesSerializer
	queryset = Solicitudes.objects.all()