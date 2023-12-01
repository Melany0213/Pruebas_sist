from rest_framework import serializers
from .models import Certification, Estudiante, Hago_Constar, Solicitud, Jurado, Folio
from .models import Profesor
import datetime

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'


class SolicitudSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(read_only=True)

    class Meta:
        model = Solicitud
        fields = '__all__'
        read_only_fields = ['certification', 'acta_equivalent', 'acta_listening', 'acta_reading', 'acta_speaking', 'acta_writing']

    def validate(self, attrs):
        now = datetime.datetime.today()
        proxima_certificacion = Certification.objects.filter(date_close_sol__gt=now)
        if not proxima_certificacion.exists():
            raise serializers.ValidationError(
                    "No hay certificacion disponible")

        # ARREGLAR FILTRAR
        estudiante = Estudiante.objects.filter(**attrs)
        # ARREGLAR FILTRAR

        if not estudiante.exists():
            raise serializers.ValidationError(
                    "No hay estudiante con esos datos")
        misma_solicitud = Solicitud.objects.filter(estudiante=estudiante[0], certification=proxima_certificacion[0])
        if misma_solicitud.exists():
            raise serializers.ValidationError(
                    "Ya ese estudiante esta en esa certificacion")
        return super().validate(attrs)
    def create(self, validated_data):
        now = datetime.datetime.today()
        proxima_certificacion = Certification.objects.filter(date_close_sol__gt=now)[0]
        estudiante = Estudiante.objects.filter(**validated_data)[0]
        return Solicitud.objects.create(certification=proxima_certificacion, estudiante=estudiante)

class ActaSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(read_only=True)

    class Meta:
        model = Solicitud
        fields = ['acta_equivalent', 'acta_listening', 'acta_reading', 'acta_speaking', 'acta_writing', 'estudiante']

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'



class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

    def validate(self, attrs):
        date_close_sol = attrs.get('date_close_sol')
        date_certification = attrs.get('date_certification')
        date_speaking = attrs.get('date_speaking')
        date_writing_reading_listening = attrs.get('date_writing_reading_listening')

        fechas = [date_close_sol, date_certification, date_speaking, date_writing_reading_listening]

        today = datetime.date.today()
        for fecha in fechas:
            print(fecha)
            if(fecha <= today):
                raise serializers.ValidationError(
                    "La certificación creada no puede  tener fecha anterior a la de hoy o igual a la de hoy")

        if(date_writing_reading_listening > date_speaking):
            raise serializers.ValidationError(
                "La fecha de las tres habilidades tiene que ser antes de la prueba oral" )

        dia_anterior = datetime.timedelta(days=1)

        print(date_close_sol - dia_anterior)

        print(date_certification)

        if(date_close_sol != date_certification - dia_anterior):
            raise serializers.ValidationError(
                "La fecha de cierre de solicitud tiene que ser el día antes del comienzo de la certifación" )

        return super().validate(attrs)


class JuradoSerializer(serializers.ModelSerializer):
    profesores_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Profesor.objects.all(), write_only=True)
    jefe_tribunal_id = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all(), allow_null=True, required=False, write_only=True)
    profesores = ProfesorSerializer(many=True, read_only=True)
    jefe_tribunal = ProfesorSerializer(allow_null=True, read_only=True)
    certification_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Certification.objects.all())

    class Meta:
        model = Jurado
        fields = '__all__'
        read_only_fields=['certification']

    def validate(self, attrs):
        tipo_tribunall= attrs.get('tipo_tribunal')
        profesores_elegidos = attrs.get('profesores_id', [])
        jefe_tribunal = attrs.get('jefe_tribunal_id')
        profesores_elegidosid=[profesor.id for profesor in profesores_elegidos]
        # print(profesores_elegidos[0].name_completo)

        certification = attrs.get('certification_id')
        juradosmismotipo=Jurado.objects.filter(tipo_tribunal=tipo_tribunall, certification=certification)

        if juradosmismotipo.exists():
            raise serializers.ValidationError(
            "Ya existe un jurado del mismo tipo para esta certificación."
        )

        for element in juradosmismotipo:
            profesores_existente = set(element.profesores.values_list('id', flat=True))
            # print(profesores_existente)
            # print(profesores_elegidosid)
            coincidencias = profesores_existente.intersection(profesores_elegidosid)
            if(coincidencias):
                raise serializers.ValidationError(
                "Alguno de los profesores elegidos ya pertenece a un tribunal del mismo tipo" )

        if jefe_tribunal and jefe_tribunal not in profesores_elegidos:
            raise serializers.ValidationError("El profesor seleccionado como jefe de tribunal debe estar en la lista de profesores elegidos.")
        return attrs

    def create(self, validated_data):
        profesores_elegidos = validated_data.pop('profesores_id', [])
        jefe_tribunal = validated_data.pop('jefe_tribunal_id', None)
        certification = validated_data.pop('certification_id', None)

        # Crear una instancia de Jurado sin el campo jefe_tribunal
        jurado = Jurado.objects.create(**validated_data, certification=certification)

        # Asignar los profesores seleccionados
        jurado.profesores.set(profesores_elegidos)

        # Asignar el jefe de tribunal seleccionado si existe
        print(profesores_elegidos, '1')
        print(jefe_tribunal)
        if jefe_tribunal:
            print(profesores_elegidos, '2')
            if (len(profesores_elegidos)==1):
                print(profesores_elegidos, '3')
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
    folio = FolioSerializer()
    class Meta:
        model = Hago_Constar
        fields = '__all__'

