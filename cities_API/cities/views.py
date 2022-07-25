from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from User.models import User

from .services import get_city_by_geoposition, VisitedPlacesPagination
from .models import City
from .serializers import CityListSerializer, CityCreateSerializer, GeolocationOutputDataSerializer, \
    GeolocationInputDataSerializer, CityUpdateSerializer

CACHE_TTL = getattr(settings, 'REDIS_CACHE_TTL', DEFAULT_TIMEOUT)


class CityView(viewsets.ViewSet):
    """City managing class"""

    pagination_class = VisitedPlacesPagination

    @swagger_auto_schema(responses={201: CityListSerializer, 400: "Bad Request"})
    def list(self, request):
        """List all cities"""
        if "city_list" in cache:
            queryset = cache.get("city_list")
        else:
            queryset = City.objects.all()
            cache.set("city_list", queryset, timeout=CACHE_TTL)
        serializer = CityListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CityCreateSerializer, responses={201: CityListSerializer, 400: "Bad Request"})
    def create(self, request):
        """Create a new city"""
        city = CityCreateSerializer(data=request.data)

        if not city.is_valid():
            return Response(status=400)

        if "city_names" in cache:
            cached_cities = cache.get("city_names")
        else:
            cached_cities = []

        city_name = city.validated_data['city_name']
        if city_name in cached_cities:
            return Response(status=201)

        cached_cities.append(city_name)
        city.save()
        cache.set("city_names", cached_cities, timeout=None)
        return Response(status=201)

    @swagger_auto_schema(request_body=CityUpdateSerializer, responses={200: "OK", 400: "Bad Request"})
    @permission_classes([IsAdminUser])
    def update(self, request):
        update_data = CityUpdateSerializer(data=request.data)
        if not update_data.is_valid():
            return Response(status=400)
        data = update_data.validated_data
        city = City.objects.get(id=data["id"])
        city.city_name = data["city_name"]
        city.latitude = data["latitude"]
        city.longitude = data["longitude"]
        city.UTC = data["UTC"]
        city.save()
        return Response(status=200)

    @swagger_auto_schema(responses={200: "OK", 404: "Not Found"})
    @permission_classes([IsAdminUser])
    def delete(self, request, city_id):
        city = get_object_or_404(City, id=city_id)
        city.delete()
        return Response(status=200)


class Geolocation(viewsets.ViewSet):
    """Locate city by longitude, latitude"""

    @swagger_auto_schema(request_body=GeolocationInputDataSerializer, responses={201: GeolocationOutputDataSerializer,
                                                                                 400: "Bad Request"})
    def get_city_by_geoposition(self, request):

        # validating input data
        data = GeolocationInputDataSerializer(data=request.data)
        if not data.is_valid():
            return Response(status=400)

        latitude = data['latitude'].value
        longitude = data['longitude'].value
        city = get_city_by_geoposition(longitude, latitude)

        # save place as visited by user
        if (not request.user.is_anonymous) and request.user.pk:
            user = User.objects.filter(id=request.user.pk)[:1].get()
            city[0].visited_by.add(user)
            city[0].save()

        # validating output data
        serializer = GeolocationOutputDataSerializer(city, many=True)
        return Response(serializer.data)


class VisitedPlaces(viewsets.ViewSet):
    """Display places, user located by Geolocation class in reverse order"""

    permission_classes = [IsAuthenticated, ]
    pagination_class = VisitedPlacesPagination

    @swagger_auto_schema(responses={201: CityListSerializer, 404: "Not Found"})
    def list(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        visited_cities = City.objects.filter(visited_by=user)
        serializer = CityListSerializer(visited_cities, many=True)
        return Response(serializer.data)

# visited places pagination, autofill
