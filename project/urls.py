from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/region/', views.region_forum, name='region_forum'),
    path('forum/school/', views.school_forum, name='school_forum'),
    path('forum/<str:forum_type>/create/', views.create_post, name='create_post'),
    path('forum/post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path("toggle-like/", views.toggle_like, name="toggle_like"),
    path('search/', views.search_page, name='search_page'),
    path('search/results/', views.search_results, name='search_results'),
    path('profile/', views.profile_page, name='profile_page'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:room_id>/', views.message_room, name='message_room'),
    path('messages/create/<int:receiver_id>/', views.create_message_room, name='create_message_room'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('reply/<int:reply_id>/edit/', views.edit_reply, name='edit_reply'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)