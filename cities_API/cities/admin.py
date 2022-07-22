from django.contrib import admin

from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_name", )


# Register your models here.
