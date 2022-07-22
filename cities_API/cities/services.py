from .models import City


def get_city_by_geoposition(longitude, latitude):
    city = City.objects.raw(f"SELECT id, city_name, abs(longitude-{longitude})+abs(latitude-{latitude})"
                            " as difference "
                            "FROM cities_city "
                            "ORDER BY difference LIMIT 1")[0:]
    return city

