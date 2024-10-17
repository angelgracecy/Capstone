from rest_framework import viewsets, permissions, filters
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import BlogPost, Category, Tag
from .serializers import BlogPostSerializer, UserSerializer, CategorySerializer, TagSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]  

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'tags']
    search_fields = ['title', 'content', 'author__username', 'tags__name']
    ordering_fields = ['published_date', 'created_date']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
           
            serializer.save(author=None)  

    @action(detail=False, methods=['get'])
    def by_author(self, request):
        author_id = request.query_params.get('author_id')
        if author_id:
            posts = BlogPost.objects.filter(author_id=author_id)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({"error": "Author ID is required"}, status=400)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            posts = BlogPost.objects.filter(category_id=category_id)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({"error": "Category ID is required"}, status=400)