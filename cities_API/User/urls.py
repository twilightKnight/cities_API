from django.urls import path
from djoser.views import UserViewSet

from .views import Login

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='create'),
    path('update/', UserViewSet.as_view({'post': 'me'}), name='update'),
    path('page/', UserViewSet.as_view({'get': 'me'}), name='user_page'),
    path('delete/', UserViewSet.as_view({'delete': 'me'}), name='delete'),

    path("login/", Login.as_view(), name="login"),

    path("activate/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "activation"}), name="activate"),
    path("resend-activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend_activation"),

    path("reset-password/", UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("reset-password-confirm/<str:uid>/<str:token>/", UserViewSet.as_view({"post": "reset_password_confirm"}),
         name="reset_password_confirm"),
]
