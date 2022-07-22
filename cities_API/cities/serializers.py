from rest_framework import serializers
import datetime

from .models import City


class CityListSerializer(serializers.ModelSerializer):
    """List of Cities"""

    current_time = serializers.SerializerMethodField('get_current_time_by_timezone')

    def get_current_time_by_timezone(self, data):
        UTC = data.UTC
        timedelta = datetime.timedelta(hours=UTC)
        timezone = datetime.timezone(offset=timedelta)
        time = datetime.datetime.now(timezone).time()
        return time.isoformat(timespec='seconds')

    class Meta:
        model = City
        fields = ("id", "city_name", "longitude", "latitude", "current_time", "UTC", )


class CityCreateSerializer(serializers.ModelSerializer):
    """Create new City"""

    class Meta:
        model = City
        fields = "__all__"


class CityUpdateSerializer(CityCreateSerializer):
    """Update city object"""

    id = serializers.IntegerField()


class GeolocationOutputDataSerializer(CityListSerializer):
    """Geolocated city data"""


class GeolocationInputDataSerializer(serializers.Serializer):
    """City coordinates"""

    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
