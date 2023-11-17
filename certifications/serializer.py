from rest_framework import serializers
from .models import Certification, Estudiante, Hago_Constar, Solicitud, Acta, Jurado, Folio
from .models import Profesor
import datetime

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'


class SolicitudSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(read_only=True)
    #acta = ActaSerializer(read_only=True, many=True)
    class Meta:
        model = Solicitud
        fields = '__all__'


class ActaSerializer(serializers.ModelSerializer):
    # solicitud = SolicitudSerializer()
    class Meta:
        model = Acta
        fields = '__all__'



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
                    "La certificación creada no puede  tener fecha anterior a la de hoy")

        if(date_writing_reading_listening > date_speaking):
            raise serializers.ValidationError(
                "asjkdnasjkdnasjkdnasjkdnasjkdna" )

        dia_anterior = datetime.timedelta(days=1)

        print(date_close_sol - dia_anterior)

        print(date_certification)

        if(date_close_sol != date_certification - dia_anterior):
            raise serializers.ValidationError(
                "asjkdnasjkdnasjkdnasjkdnasjkdna2" )

        return super().validate(attrs)


class JuradoSerializer(serializers.ModelSerializer):
    profesores_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Profesor.objects.all(), write_only=True)
    jefe_tribunal_id = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all(), allow_null=True, required=False, write_only=True)
    profesores = ProfesorSerializer(many=True, read_only=True)
    jefe_tribunal = ProfesorSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Jurado
        fields = '__all__'

    def validate(self, attrs):
        tipo_tribunall= attrs.get('tipo_tribunal')
        profesores_elegidos = attrs.get('profesores_id', [])
        jefe_tribunal = attrs.get('jefe_tribunal_id')
        profesores_elegidosid=[profesor.id for profesor in profesores_elegidos]
        # print(profesores_elegidos[0].name_completo)

        juradosmismotipo=Jurado.objects.filter(tipo_tribunal=tipo_tribunall)

        print(juradosmismotipo)
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
    folio = FolioSerializer()
    class Meta:
        model = Hago_Constar
        fields = '__all__'

