from django.test import TestCase
from rest_framework.test import APIClient
from .models import Estudiante, Profesor, Certification, Acta, Solicitud, Jurado, Folio, Hago_Constar

class EstudianteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.estudiante = Estudiante.objects.create(/* tus datos de prueba */)

    def test_get_estudiante(self):
        response = self.client.get(f'/api/estudiante/{self.estudiante.id}/')
        self.assertEqual(response.status_code, 200)

class ProfesorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profesor = Profesor.objects.create(/* tus datos de prueba */)

    def test_get_profesor(self):
        response = self.client.get(f'/api/profesor/{self.profesor.id}/')
        self.assertEqual(response.status_code, 200)

class CertificationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.certification = Certification.objects.create(/* tus datos de prueba */)

    def test_get_certification(self):
        response = self.client.get(f'/api/certification/{self.certification.id}/')
        self.assertEqual(response.status_code, 200)

class ActaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.acta = Acta.objects.create(/* tus datos de prueba */)

    def test_get_acta(self):
        response = self.client.get(f'/api/acta/{self.acta.id}/')
        self.assertEqual(response.status_code, 200)

class SolicitudTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.solicitud = Solicitud.objects.create(/* tus datos de prueba */)

    def test_get_solicitud(self):
        response = self.client.get(f'/api/solicitud/{self.solicitud.id}/')
        self.assertEqual(response.status_code, 200)

class JuradoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.jurado = Jurado.objects.create(/* tus datos de prueba */)

    def test_get_jurado(self):
        response = self.client.get(f'/api/jurado/{self.jurado.id}/')
        self.assertEqual(response.status_code, 200)

class FolioTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.folio = Folio.objects.create(/* tus datos de prueba */)

    def test_get_folio(self):
        response = self.client.get(f'/api/folio/{self.folio.id}/')
        self.assertEqual(response.status_code, 200)

class Hago_ConstarTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.hago_constar = Hago_Constar.objects.create(/* tus datos de prueba */)

    def test_get_hago_constar(self):
        response = self.client.get(f'/api/hago_constar/{self.hago_constar.id}/')
        self.assertEqual(response.status_code, 200)