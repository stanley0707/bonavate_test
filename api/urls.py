from django.urls import path
from rest_framework import routers

from .views import clients

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'client', clients.ClientAccountViewSet, basename='client')

urlpatterns = router.urls