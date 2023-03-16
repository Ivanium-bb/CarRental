from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import date
from Main.models import Car, Session
from Main.consts import *


class CarTests(APITestCase):

    def test_CheckAvailableCar(self):
        car1 = Car.objects.create(is_available=True)
        car2 = Car.objects.create(is_available=False)
        url = reverse('available', kwargs={'pk': car1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, True)

        url = reverse('available', kwargs={'pk': car2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, False)

    def test_CalculatePrice(self):
        url = reverse('price')
        data = {'session_start': '2021-04-02',
                'session_finish': '2021-03-31'}
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, finish_before)

        data = {'session_start': '2021-03-01',
                'session_finish': '2021-03-31'}
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, long_period)

        data = {'session_start': '2023-03-10',
                'session_finish': '2023-03-18'}
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, finish_we)

        data = {'session_start': '2023-03-11',
                'session_finish': '2023-03-24'}
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, start_we)

        data = {'session_start': '2021-03-02',
                'session_finish': '2021-03-31'}
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, 26150)

    def test_CreateSession(self):
        car1 = Car.objects.create(is_available=True)
        car2 = Car.objects.create(is_available=False)
        Session.objects.create(session_start=date(2023, 3, 16),
                               session_finish=date(2023, 3, 23),
                               car_id=car1.id)
        url = reverse('session')

        data = {'session_start': '2021-04-02',
                'session_finish': '2021-03-31',
                'car': car2.id
                }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, not_available)

        data = {'session_start': '2023-03-24',
                'session_finish': '2023-03-28',
                'car': car1.id
                }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.data, '3 days are not over yet')

        data = {'session_start': '2023-03-27',
                'session_finish': '2023-03-28',
                'car': car1.id
                }
        response = self.client.post(path=url, data=data)

        self.assertEqual(response.data, {
            "id": 2,
            "session_start": "2023-03-27",
            "session_finish": "2023-03-28",
            "car": car1.id
        })

    def test_Statistic(self):
        url = reverse('statistic')

        # Session start and finish in previous month
        Session.objects.create(session_start=date(2023, 2, 16),
                               session_finish=date(2023, 2, 23),
                               car_id=1)  # 0 days 0%

        # Session start and finish in current month
        Session.objects.create(session_start=date(2023, 3, 1),
                               session_finish=date(2023, 3, 21),
                               car_id=1)  # 21 days 67%

        # Session start in previous month
        Session.objects.create(session_start=date(2023, 2, 27),
                               session_finish=date(2023, 3, 7),
                               car_id=2)  # 7 days 22%

        # Session finish in present month
        Session.objects.create(session_start=date(2023, 3, 29),
                               session_finish=date(2023, 4, 10),
                               car_id=3)  # 3 days 9% total 32%
        response = self.client.get(path=url)

        result = {
            'report for evey car': {
                'Car id:1': 'Days in rent 67%',
                'Car id:2': 'Days in rent 22%',
                'Car id:3': 'Days in rent 9%',
                'Car id:4': 'Days in rent 0%',
                'Car id:5': 'Days in rent 0%',

            },
            'report for all cars together': '19%'
        }
        self.assertEqual(response.data, result)
