from django.db import models

# Create your models here.
class Line(models.Model):                    # model - class    - table
    text = models.CharField(max_length=255)  # field - instance - row

