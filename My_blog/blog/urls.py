from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, TagViewSet, BlogPostViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', BlogPostViewSet)



urlpatterns = [
    path('', include(router.urls)),
]