from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo','imagen', 'descripcion', 'relevante']
        #widgets = {
        #    'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        #    'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        #    'relevante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        #}