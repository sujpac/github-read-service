from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.TopNReposViewSet, basename='top-n-repos-viewset')

urlpatterns = [
    path('top/<int:N>/', include(router.urls)),
]
