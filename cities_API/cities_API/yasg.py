from django.urls import path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Cities API",
      default_version='v1',
      description="Test description",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[AllowAny, ],
)

urlpatterns = [
   path('docs/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]