from django.contrib import admin
from .models import Post, Categoria
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("subida", "comentario")

admin.site.register(Categoria)
admin.site.register(Post, PostAdmin)