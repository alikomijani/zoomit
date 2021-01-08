from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import home, post_single, categories_archive, category_single, like_comment, PostArchive, PostDetails, \
    CategoryDetails, create_comment

from .api import PostViewSet, CategoryViewSet, CommentViewSet
from zoomit.urls import router

router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('posts/', PostArchive.as_view(), name='posts_archive'),
    path('post/<slug:slug>/', post_single, name='post_single'),
    path('categories/', categories_archive, name='categories_archive'),
    # path('categories/<slug:pk>/', category_single, name='category_single'),
    path('categories/<slug:slug>/',
         CategoryDetails.as_view(), name='category_single'),
    path('like_comment/', like_comment, name='like_comment'),
    path('comments/', create_comment, name='add_comment'),

]
