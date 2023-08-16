from django.urls import path
from rest_framework.routers import DefaultRouter
from mock_exchange_app.users.views import me, UsersViewSet, google_login, update_profile_img, get_profile_image_signed_url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from mock_exchange_app.wallets.views import WalletsViewSet

router = DefaultRouter()
router.register('', WalletsViewSet)


urlpatterns = [
]

urlpatterns.extend(router.urls)