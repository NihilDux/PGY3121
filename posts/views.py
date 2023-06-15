from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import PostForm
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    posts = Post.objects.filter(dateaprobado__isnull=False).order_by('-dateaprobado')
    return render(request, 'home.html', {'posts': posts})

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('posts')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error": 'Contraseñas no coinciden.'
                })  
@login_required           
def posts(request):
    posts = Post.objects.filter(user=request.user, dateaprobado__isnull=True)
    return render(request, 'posts.html', {'posts': posts})

def posts_published(request):
    posts = Post.objects.filter(dateaprobado__isnull=False).order_by('-dateaprobado')
    return render(request, 'posts.html', {'posts': posts})
@login_required 
def create_post(request):
    if request.method == 'POST':
        try:
            form = PostForm(request.POST, request.FILES)  # Agregar request.FILES al inicializar el formulario
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                print(request.POST, request.FILES)
                return redirect('posts')
        except ValueError:
            print(request.POST)
            return render(request, 'create_post.html', {
                'form': PostForm(),
                'error': 'Por favor, valide los datos'
            })
    else:
        return render(request, 'create_post.html', {
            'form': PostForm()
        })

def post_detail(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id, user=request.user)
        form = PostForm(instance=post)
        return render(request, 'post_detail.html',{
            'post':post,
            'form': form
            })
    else:
        try:
            post = get_object_or_404(Post, pk=post_id, user=request.user)
            form = PostForm(request.POST, instance=post)
            form.save()
            return redirect('posts')
        except ValueError:
                return render(request, 'post_detail.html',{
                'post':post,
                'form': form,
                'error': 'Error al Actualizar'
                })
@login_required 
def published_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == 'POST':
        post.dateaprobado = timezone.now()
        post.save()
        return redirect('posts')
@login_required 
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
@login_required 
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
         })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('posts')
            

        