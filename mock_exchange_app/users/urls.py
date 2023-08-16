from django.urls import path
from rest_framework.routers import DefaultRouter
from mock_exchange_app.users.views import me, UsersViewSet, google_login, update_profile_img, get_profile_image_signed_url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

router = DefaultRouter()
router.register('', UsersViewSet)


urlpatterns = [
    path('google-auth', google_login),
    path('tokens', TokenObtainPairView.as_view()),
    path('me', me),
    path('profile/img', get_profile_image_signed_url),
    path('profile/img/done', update_profile_img)
]

urlpatterns.extend(router.urls)