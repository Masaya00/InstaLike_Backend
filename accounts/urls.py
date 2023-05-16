from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserView, UserViewSet


# 追加
router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('user/', UserView.as_view()),
]