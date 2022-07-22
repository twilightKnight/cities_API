from django.urls import path

from . import views

urlpatterns = [
    path("cities/", views.CityView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path("cities/<int:city_id>", views.CityView.as_view({'delete': 'delete'})),

    path("location/", views.Geolocation.as_view({'post': 'get_city_by_geoposition'})),
    path("visited_places", views.VisitedPlaces.as_view({'get': 'list'}))
]
