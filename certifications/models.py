import datetime
from django.db import models
from django.forms import ValidationError
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from main_app.admin import User
from django.utils import timezone


# Create your models here.
class Estudiante(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    year = models.CharField(max_length=4)
    group = models.CharField(max_length=10)
    name = models.CharField(max_length=15)
    second_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=35)
    second_surname = models.CharField(max_length=35)
    decano = models.CharField(max_length=150)
    career = models.CharField(max_length=150)

class Profesor(models.Model):
    name_completo = models.CharField(max_length=150)
    facultad = models.PositiveIntegerField(default=0)

class Certification(models.Model):
    date_close_sol = models.DateField()#Comienza la certificacion 1 dia despues
    date_certification = models.DateField(default= datetime.date.today)
    date_speaking = models.DateField()
    date_wiriting_reading_listening = models.DateField()

    def save(self, *args, **kwargs):
        self.date_close_sol = Certification.objects.latest('date_certification').date_certification
        super().save(*args, **kwargs)

class Acta(models.Model):
    NOTES_CHOICES = [
        ("Basic  1","A1"),
        ("Basic  2", "A2"),
        ("Intermediate", "B1"),
        ("Upper Intermediate", "B2"),
        ("Advanced", "C1"),
    ]
    reading = models.CharField( choices = NOTES_CHOICES, max_length=20)
    listening = models.CharField( choices = NOTES_CHOICES, max_length=20)
    writing = models.CharField( choices = NOTES_CHOICES, max_length=20)
    speaking = models.CharField( choices = NOTES_CHOICES, max_length=20)
    equivalent = models.CharField(max_length=35)

class Solicitud(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, default=0)
    certification = models.ForeignKey(
        Certification, on_delete=models.CASCADE, default=0)
    acta = models.ManyToManyField( Acta, blank=True)
    date_has_solicitud = models.DateField()

    #Guardo la fecha de la solicitud con la fecha actual del sistema
    def clean(self):
        if self.date_has_solicitud >= self.certification.date_close_sol:
            raise ValidationError("La solicitud realizada debe ser hecha antes de la fecha de cierre de las mismas")

    def save(self, *args, **kwargs):
        self.date_has_solicitud = timezone.now().date()
        super().save(*args, **kwargs)

class Jurado(models.Model):
    TIPO_TRIBUNAL_CHOICES = [
        ("Examenes escritos",  "Exámenes de las 4 habilidades"),
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
        # # Verifica que solo se elija un profesor como jefe de tribunal
        # if self.jefe_tribunal and self.jefe_tribunal not in self.profesores.all():
        #     raise ValidationError(
        #         "El profesor seleccionado como jefe de tribunal debe estar en la lista de profesores del tribunal." )

    # def save(self, *args, **kwargs):
    #     # Verifica si el tribunal tiene solo un profesor y asignar None a jefe_tribunal si es así
    #     if self.profesores.count() == 1:
    #             self.jefe_tribunal = None
    #     super().save(*args, **kwargs)

class Folio(models.Model):
    tomo = models.IntegerField(validators=[MaxValueValidator(100)])
    numero = models.IntegerField()

class Hago_Constar(models.Model):
    estudiante = models.OneToOneField(
        Estudiante, on_delete=models.CASCADE, default=0)
    emision = models.DateField()
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, null=True)

    def clean(self):
        super().clean()
        if Hago_Constar.objects.filter(folio=self.folio).count() >= 20:
            raise ValidationError("Se ha alcanzado el límite de certificaciones para este folio.")