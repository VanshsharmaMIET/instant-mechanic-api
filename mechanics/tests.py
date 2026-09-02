from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Mechanic


class MechanicAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.mechanic = Mechanic.objects.create(
            name="Test Garage", phone="9876543210", location="Delhi",
            rating=4.0, is_open=True, services=["Oil Change"]
        )

    def test_list_mechanics(self):
        response = self.client.get('/api/mechanics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_mechanic_invalid_phone(self):
        data = {"name": "Bad Phone", "phone": "12345", "location": "Delhi",
                "rating": 4, "is_open": True, "services": ["AC Repair"]}
        response = self.client.post('/api/mechanics/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_service_request_invalid_mechanic(self):
        data = {"customer_name": "Amit", "customer_phone": "9123456780",
                "vehicle_number": "UP16AB1234", "mechanic": 999,
                "service": "Oil Change", "problem_description": "test"}
        response = self.client.post('/api/service-requests/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_service_request_invalid_service(self):
        data = {"customer_name": "Amit", "customer_phone": "9123456780",
                "vehicle_number": "UP16AB1234", "mechanic": self.mechanic.id,
                "service": "Painting", "problem_description": "test"}
        response = self.client.post('/api/service-requests/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)