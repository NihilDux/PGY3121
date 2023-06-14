
from django.contrib import admin
from django.urls import path
from posts import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('posts/', views.posts, name='posts'),
    path('posts_published/', views.posts_published, name='posts_published'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/published', views.published_post, name='published_post'),
    path('posts/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]