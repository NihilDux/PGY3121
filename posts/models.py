from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='posts/', null=True, blank=True)
    descripcion = models.TextField(blank=True)
    subida = models.DateTimeField(auto_now_add=True)
    dateaprobado = models.DateTimeField(null=True, blank=True)
    relevante = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - Por ' + self.user.username