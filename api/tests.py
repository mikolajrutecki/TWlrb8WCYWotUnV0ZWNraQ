import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import RequestModel


class RequestTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_data = {'url': 'https://httpbin.org/range/15', 'interval': 60}
        self.response = self.client.post(
            reverse('api:fetcher-list'),
            self.request_data,
            format="json"
        )

    def test_api_can_create_request(self):
        """
        Test if API can create RequestModel object
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_request(self):
        """
        Test if API can get RequestModel object
        """
        req = RequestModel.objects.get()
        response = self.client.get(
            reverse('api:fetcher-detail',
                    kwargs={'pk': req.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_update_request(self):
        """
        Test if API can update given RequestModel object
        """
        req = RequestModel.objects.get()
        change_req = {'url': 'https://httpbin.org/delay/5', 'interval': 15}
        res = self.client.put(
            reverse('api:fetcher-detail', kwargs={'pk': req.id}),
            change_req, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_request(self):
        """
        Test if API can delete given RequestModel object
        """
        req = RequestModel.objects.get()
        response = self.client.delete(
            reverse('api:fetcher-detail', kwargs={'pk': req.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_get_wrong_request_id(self):
        """
        Test if API can handle wrong query(wrong PK)
        """
        response = self.client.get(
            reverse('api:fetcher-detail', kwargs={'pk': 'test'}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_create_request_wrong_json(self):
        """
        Test if API can handle wrong POST(wrong JSON)
        """
        client = APIClient()
        request_data = {'test1': 'https://httpbin.org/range/15', 'test2': 60}
        response = client.post(
            reverse('api:fetcher-list'),
            request_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

