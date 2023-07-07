from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    id_categoria  = models.AutoField(db_column='idCategoria', primary_key=True) 
    categoria     = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.categoria)


class Post(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField(null=True)
    imagen = models.ImageField(upload_to='posts/', null=True, blank=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    subida = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    relevante = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #imagen = models.ImageField(upload_to='media', default='default.jpg') -- IGNORAR

    def __str__(self):
        return self.titulo + ' - Por ' + self.user.username


class CarritoItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.PositiveIntegerField(default=0)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.post.titulo} - {self.usuario.username if self.usuario else 'Usuario Anónimo'}"
