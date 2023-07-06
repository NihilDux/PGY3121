
from django.contrib import admin
from django.urls import path
from posts import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contacto', views.contacto, name='contacto'),
    path('signup/', views.signup, name='signup'),
    path('posts/', views.posts, name='posts'),
    path('pending_posts/', views.pending_posts, name='pending_posts'),
    path('posts_published/', views.posts_published, name='posts_published'),
    #path('posts/<int:categoria_id>/', views.post_por_categoria, name='categoria'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/detail/<int:post_id>/', views.detail, name='detail'),
    path('posts/<int:post_id>/published', views.published_post, name='published_post'),
    path('posts/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('buscar/', views.buscar, name='buscar'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:post_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:carritoitem_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

