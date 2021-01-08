from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PostModelSerializer, CommentModelSerializer, CategoryModelSerializer
from .models import Post, Comment, Category

from rest_framework.viewsets import ModelViewSet


class PostViewSet(ModelViewSet):
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()

    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentModelSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.draft = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_published(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(draft=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.filter(is_confirmed=True)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
