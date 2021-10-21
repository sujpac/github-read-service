from django.urls import path, include

from rest_framework.routers import DefaultRouter

from repo_api import views


router = DefaultRouter()
router.register('', views.RepoRankViewSet, basename='repo-rank-viewset')

urlpatterns = [
    path('top/<int:N>/', include(router.urls)),
]
