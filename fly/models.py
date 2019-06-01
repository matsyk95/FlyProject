from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

from django.db import models
from django.urls import reverse

class Country(models.Model):
    name = models.CharField(max_length=40)
    name2 = models.CharField(max_length=40, blank=True)
    name3 = models.CharField(max_length=40, blank=True)
    name4 = models.CharField(max_length=40, blank=True)
    country_logo = models.FileField(blank=True)
    def __str__(self):
        return '{}'.format(self.name)



class Fly(models.Model):
    CURRENCY_CHOICES= (
        ('PLN', 'PLN'),
        ('USD', 'USD')
    )
    orginplace = models.CharField(max_length=40, blank=True, default="Warsaw", help_text="Start place")
    descinationplace = models.CharField(max_length=40, blank=False)
    year = models.IntegerField(blank=True, default=0)
    month = models.IntegerField(blank=True, default=0)
    day = models.IntegerField(blank=True, default=0)
    price = models.IntegerField(blank=True, default=0, null=True)
    currency = models.CharField(max_length=40, choices=CURRENCY_CHOICES)
    date = models.DateField(default=datetime.date.today, blank=True)
    number_city = models.IntegerField(blank=True, default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    airports = models.ForeignKey(Country, on_delete=models.CASCADE, default="", blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)

    @property
    def is_in_base(self):
        return self.day >0


