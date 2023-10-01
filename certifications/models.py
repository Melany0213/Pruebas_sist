from django.db import models

# Create your models here.
class Estudiante(models.Model):
    year = models.CharField(max_length=4)
    group = models.CharField(max_length=10)
    name = models.CharField(max_length=15)
    second_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=35)
    second_surname = models.CharField(max_length=35)
    reading = models.CharField(max_length=3)
    listening = models.CharField(max_length=3)
    writing = models.CharField(max_length=3)
    speaking = models.CharField(max_length=3)
    equivalent = models.CharField(max_length=35)
    tomo = models.PositiveIntegerField()
    folio = models.PositiveIntegerField()
    decano = models.CharField(max_length=150)
    court_president = models.CharField(max_length=150)
    career = models.CharField(max_length=150)

class Profesor(models.Model):
    name = models.CharField(max_length=15)
    second_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=35)
    second_surname = models.CharField(max_length=35)
    facultad = models.PositiveIntegerField(default=1)
class Certifications(models.Model):
    date = models.DateField()
    cant_est = models.IntegerField()
    cant_sol = models.IntegerField()
    aprobados = models.IntegerField()

class Hago_Constar(models.Model):
    emision = models.DateField()
    #datos de los estudiantes, todos

class Solicitudes(models.Model):
    #datos de los estudiantes(nombre, apellidos y facultad)
    date = models.DateField()
