from django.db import models
from User.models import User


class City(models.Model):
    """Base City model"""

    city_name = models.CharField(max_length=50)
    longitude = models.FloatField()
    latitude = models.FloatField()
    UTC = models.SmallIntegerField()
    visited_by = models.ManyToManyField(User, default=None)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

