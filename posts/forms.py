from django import forms
from .models import Post, Categoria
from django.forms import ModelForm

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"
        labels = {'categoria':'Categoria',}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'descripcion', 'precio','imagen','aprobado', 'relevante', 'comentario', 'id_categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control'}),
            'id_categoria': forms.Select(attrs={'class': 'form-select'}),
        }