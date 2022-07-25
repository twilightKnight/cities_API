from rest_framework.response import Response

from .models import City
from rest_framework.pagination import PageNumberPagination


def get_city_by_geoposition(longitude: float, latitude: float) -> City:
    """Return city object closest to provided longitude, latitude"""

    city = City.objects.raw(f"SELECT id, city_name, abs(longitude-{longitude})+abs(latitude-{latitude})"
                            " as difference "
                            "FROM cities_city "
                            "ORDER BY difference LIMIT 1")[0:]
    return city


class VisitedPlacesPagination(PageNumberPagination):
    """Pagination class for Visited Cities API call"""

    page_size = 3
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'result': data
        })

