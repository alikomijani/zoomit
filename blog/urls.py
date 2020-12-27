from django.urls import path
from .views import home, post_single, categories_archive, category_single, like_comment, PostArchive, PostDetails, \
    CategoryDetails , create_comment

urlpatterns = [
    path('', home, name='home'),
    path('posts/', PostArchive.as_view(), name='posts_archive'),
    path('post/<slug:slug>/', post_single, name='post_single'),
    path('categories/', categories_archive, name='categories_archive'),
    # path('categories/<slug:pk>/', category_single, name='category_single'),
    path('categories/<slug:slug>/', CategoryDetails.as_view(), name='category_single'),
    path('like_comment/', like_comment, name='like_comment'),
    path('comments/', create_comment, name='add_comment'),

]
