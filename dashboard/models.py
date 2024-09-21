from django.db import models

# Create your models here.


class Config(models.Model):
    tax=models.DecimalField(max_digits=5, decimal_places=2)
    