from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment, PostSetting
from account.serializers import UserSerializer

User = get_user_model()


class PostSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostSetting
        fields = "__all__"


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostModelSerializer(serializers.ModelSerializer):
    post_setting = PostSettingSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
