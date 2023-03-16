from django.db import models


class Car(models.Model):
    is_available = models.BooleanField()


class Session(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    session_start = models.DateField(blank=True)
    session_finish = models.DateField(blank=True)
