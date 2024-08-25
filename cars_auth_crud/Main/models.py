from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Maker(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100)
    mileage = models.IntegerField()
    comments = models.TextField()
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)

    def __str__(self):
        return self.car_model
