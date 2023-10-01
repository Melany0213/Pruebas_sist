from rest_framework import serializers
from .models import Certifications, Estudiante, Hago_Constar, Solicitudes
from .models import Profesor

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        # fields = ('id', 'title', 'description', 'done')
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        # fields = ('id', 'title', 'description', 'done')
        fields = '__all__'

class CertificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certifications
        # fields = ('id', 'title', 'description', 'done')
        fields = '__all__'

class Hago_ConstarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hago_Constar
        # fields = ('id', 'title', 'description', 'done')
        fields = '__all__'

class SolicitudesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitudes
        # fields = ('id', 'title', 'description', 'done')
        fields = '__all__'