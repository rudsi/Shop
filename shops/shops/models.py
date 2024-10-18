from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Shop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text = "Latitude must be between -90 and 90."
    )
    longitude = models.FloatField(
        validators= [MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text = "Longitude must be between -180 and 180."
    )

    def __str__(self):
        return self.name