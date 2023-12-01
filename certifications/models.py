import datetime
from django.db import models
from django.forms import ValidationError
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from main_app.models import User
#from django.utils import timezone


# Create your models here.
class Estudiante(models.Model):
    FACULTAD_CHOICES = [
        ("Facultad 1","F1"),
        ("Facultad  2", "F2"),
        ("Facultad 3", "F3"),
        ("Facultad 4", "F4"),
        ("Facultad FTE", "FTE"),
        ("Facultad CITEC", "CITEC"),
    ]
    CARRERA_CHOICES = [
        ("Ingeniería en Ciencias Informáticas","ICI"),
        ("Ingeniería en Bioinformática", "BIO"),
        ("Redes y seguridad informática", "ARSI"),
        ("Ingeniería en Ciberseguridad", "Ciber"),
    ]
    year = models.CharField(max_length=4)
    group = models.CharField(max_length=10)
    facultad = models.CharField(choices = FACULTAD_CHOICES, max_length=100, blank=True, null=True)
    name = models.CharField(max_length=15)
    second_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=35)
    second_surname = models.CharField(max_length=35)
    decano = models.CharField(max_length=150)
    career = models.CharField(choices = CARRERA_CHOICES , max_length=100)

    @property
    def ultima_solicitud(self):
        solicitud = Solicitud.objects.filter(estudiante=self).order_by('-date_has_solicitud')
        return solicitud[0] if solicitud.exists() else None



class Profesor(models.Model):
    name_completo = models.CharField(max_length=150)
    facultad = models.PositiveIntegerField(default=0)

class Certification(models.Model):
    date_close_sol = models.DateField(unique=True)#Comienza la certificacion 1 dia despues
    date_certification = models.DateField(unique=True)
    date_speaking = models.DateField(unique=True)
    date_writing_reading_listening = models.DateField(unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Solicitud(models.Model):
    estudiante = models.ForeignKey("certifications.Estudiante", on_delete=models.CASCADE)
    certification = models.ForeignKey("certifications.Certification", on_delete=models.CASCADE)
    date_has_solicitud = models.DateField(auto_now=True)
    NOTES_CHOICES = [
        ("Basic  1","A1"),
        ("Basic  2", "A2"),
        ("Intermediate", "B1"),
        ("Upper Intermediate", "B2"),
        ("Advanced", "C1"),
    ]
    acta_reading = models.CharField( choices = NOTES_CHOICES, max_length=20, default='')
    acta_listening = models.CharField( choices = NOTES_CHOICES, max_length=20, default='')
    acta_writing = models.CharField( choices = NOTES_CHOICES, max_length=20, default='')
    acta_speaking = models.CharField( choices = NOTES_CHOICES, max_length=20, default='')
    acta_equivalent = models.CharField(max_length=35, default='')

    #Guardo la fecha de la solicitud con la fecha actual del sistema
    def clean(self):
        if self.date_has_solicitud >= self.certification.date_close_sol:
            raise ValidationError("La solicitud realizada debe ser hecha antes de la fecha de cierre de las mismas")


class Jurado(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    TIPO_TRIBUNAL_CHOICES = [
        ("Examenes escritos",  "Exámenes de las 3 habilidades"),
        ("Examen oral",  "Examen oral (speaking)"),
        ("Calificación de escucha", "Calificación de escucha (listening)"),
        ("Calificación de escritura", "Calificación de escritura (writing)"),
        ("Calificación de lectura", "Calificación de lectura (reading)"),
        ("Otorgar nivel", "Dado el nivel de las 4 habilidades, dar nivel final"),
    ]
    tipo_tribunal = models.CharField(max_length=25, choices=TIPO_TRIBUNAL_CHOICES)
    profesores = models.ManyToManyField(Profesor, blank=True)
    jefe_tribunal = models.ForeignKey(Profesor, on_delete=models.CASCADE, null=True, blank=True, related_name='jefe_tribunal')

    def clean(self):
        super().clean()

        juradosmismotipo=Jurado.objects.filter(tipo_tribunal=self.tipo_tribunal)
        for element in juradosmismotipo:
            profesores_existente = set(element.profesores.values_list('id', flat=True))
            profesores_actuales = set(self.profesores.values_list('id', flat=True))
            coincidencias = profesores_existente.intersection(profesores_actuales)
            if(coincidencias):
                raise ValidationError(
                "Alguno de los profesores elegidos ya pertenece a un tribunal del mismo tipo" )

class Folio(models.Model):
    tomo = models.IntegerField(validators=[MaxValueValidator(100)])
    numero = models.IntegerField()

class Hago_Constar(models.Model):
    estudiante = models.OneToOneField(
        Estudiante, on_delete=models.CASCADE)
    emision = models.DateField(auto_now=True)
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, null=True)

    def clean(self):
        super().clean()
        if Hago_Constar.objects.filter(folio=self.folio).count() >= 20:
            raise ValidationError("Se ha alcanzado el límite de certificaciones para este folio.")