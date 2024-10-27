from django.urls import path
from forum.views import (
    forum_view, 
    create_post_view, 
    post_detail_view,
    edit_post_view,
    delete_post_view,
    edit_comment_view,
    delete_comment_view
)

app_name = 'forum'

urlpatterns = [
    path('forum/', forum_view, name='forum_view'),
    path('forum/create/', create_post_view, name='create_post'),
    path('forum/post/<int:post_id>/', post_detail_view, name='post_detail'),
    path('forum/post/edit/<int:post_id>/', edit_post_view, name='edit_post'),
    path('forum/post/delete/<int:post_id>/', delete_post_view, name='delete_post'),
    path('forum/comment/edit/<int:comment_id>/', edit_comment_view, name='edit_comment'),
    path('forum/comment/delete/<int:comment_id>/', delete_comment_view, name='delete_comment'),
]