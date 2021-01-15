from django.http import HttpResponse, JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostModelSerializer, CommentModelSerializer, CategoryModelSerializer
from .models import Post, Comment, Category
from .permissions import IsPostAuthorOrReadOnly
from rest_framework.viewsets import ModelViewSet


class PostViewSet(ModelViewSet):
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    permission_classes = [IsPostAuthorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']

    # authentication_classes = ()
    # def get_queryset(self):
    #     queryset = super(PostViewSet, self).get_queryset()
    #     return queryset.filter(author=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super(PostViewSet, self).get_queryset()
        allow_discussion = self.request.query_params.get('allow_discussion', None)
        if allow_discussion == 'true':
            queryset = queryset.filter(post_setting__allow_discussion=True)
        else:
            queryset = queryset.filter(post_setting__allow_discussion=False)
        return queryset

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
    permission_classes = [IsAuthenticated]
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.filter(is_confirmed=True)


class CategoryViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
