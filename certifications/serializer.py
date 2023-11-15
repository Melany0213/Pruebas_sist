from rest_framework import serializers
from .models import Certification, Estudiante, Hago_Constar, Solicitud, Acta, Jurado, Folio
from .models import Profesor

class ActaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Acta
        fields = '__all__'

class SolicitudSerializer(serializers.ModelSerializer):
    acta = ActaSerializer(read_only=True, many=True)
    class Meta:
        model = Solicitud
        fields = '__all__'


class EstudianteSerializer(serializers.ModelSerializer):
    solicitudes = SolicitudSerializer(many=True, read_only=True)
    class Meta:
        model = Estudiante
        fields = '__all__'


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class JuradoSerializer(serializers.ModelSerializer):
    profesores = serializers.PrimaryKeyRelatedField(many=True, queryset=Profesor.objects.all())
    jefe_tribunal = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all(), allow_null=True, required=False)
    # profesores = ProfesorSerializer(many=True)
    # jefe_tribunal = ProfesorSerializer(allow_null=True)

    class Meta:
        model = Jurado
        fields = '__all__'

    def validate(self, attrs):
        tipo_tribunall= attrs.get('tipo_tribunal')
        profesores_elegidos = attrs.get('profesores', [])
        jefe_tribunal = attrs.get('jefe_tribunal')
        profesores_elegidosid=[profesor.id for profesor in profesores_elegidos]
        print(profesores_elegidos[0].name_completo)
        juradosmismotipo=Jurado.objects.filter(tipo_tribunal=tipo_tribunall)
        for element in juradosmismotipo:
            profesores_existente = set(element.profesores.values_list('id', flat=True))
            print(profesores_existente)
            print(profesores_elegidosid)
            coincidencias = profesores_existente.intersection(profesores_elegidosid)
            if(coincidencias):
                raise serializers.ValidationError(
                "Alguno de los profesores elegidos ya pertenece a un tribunal del mismo tipo" )
        if jefe_tribunal and jefe_tribunal not in profesores_elegidos:
            raise serializers.ValidationError("El profesor seleccionado como jefe de tribunal debe estar en la lista de profesores elegidos.")
        return attrs

    class Meta:
        model = Jurado
        fields = '__all__'

    def create(self, validated_data):
        profesores_elegidos = validated_data.pop('profesores', [])
        jefe_tribunal = validated_data.pop('jefe_tribunal', None)

        # Crear una instancia de Jurado sin el campo jefe_tribunal
        jurado = Jurado.objects.create(**validated_data)

        # Asignar los profesores seleccionados
        jurado.profesores.set(profesores_elegidos)

        # Asignar el jefe de tribunal seleccionado si existe
        if jefe_tribunal:
            if (len(profesores_elegidos)==1):
                jurado.jefe_tribunal=None
            else:
                jurado.jefe_tribunal=jefe_tribunal
            jurado.save()

        return jurado


class FolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folio
        fields = '__all__'


class Hago_ConstarSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()
    class Meta:
        model = Hago_Constar
        fields = '__all__'

