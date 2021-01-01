from django.urls import path
from .views import home, post_single, categories_archive, category_single, like_comment, PostArchive, PostDetails, \
    CategoryDetails, create_comment

from .api import post_list, post_detail, comment_detail, comment_list

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
    path('json/posts/', post_list, name='posts_list'),
    path('json/posts/<int:pk>', post_detail, name='post_detail'),
    path('json/comments/', comment_list, name='comments_list'),
    path('json/comments/<int:pk>', comment_detail, name='comment_detail'),
]
