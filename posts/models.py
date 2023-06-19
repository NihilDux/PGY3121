from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    id_categoria  = models.AutoField(db_column='idCategoria', primary_key=True) 
    categoria     = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.categoria)

class Post(models.Model):
    titulo       = models.CharField(max_length=100)
    descripcion  = models.TextField(blank=True)
    precio       = models.CharField(max_length=100, null=True)
    imagen       = models.ImageField(upload_to='posts/', null=True, blank=True)
    id_categoria = models.ForeignKey('Categoria',on_delete=models.CASCADE, db_column='idCategoria', null=True)
    subida       = models.DateTimeField(auto_now_add=True)
    aprobado     = models.BooleanField(default=False)
    relevante    = models.BooleanField(default=False)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + ' - Por ' + self.user.username