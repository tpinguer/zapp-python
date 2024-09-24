from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

class YourAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_documents(self):
        """Teste para verificar se a API retorna os documentos corretamente"""
        url = reverse('list_documents') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_document(self):
        """Teste para verificar se a API cria um novo documento corretamente"""
        data = {
          'name': 'Novo Documento',
          'url_pdf': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
          'signers': [
              {'name': 'John Doe', 'email': 'john@example.com'},
              {'name': 'Jane Doe', 'email': 'jane@example.com'}
          ]
        }
        response = self.client.post(reverse('create_document'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data['message'], "Documento criado com sucesso")
