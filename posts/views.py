from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.db import IntegrityError
from django.db.models import Count
from .forms import PostForm
from .models import Post, Categoria, CarritoItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
from django.db.models import Q

def superuser_check(user):
    return user.is_superuser

#@user_passes_test(superuser_check)

def agregar_al_carrito(request, post_id): # Falta agregar de que no redirija y solo lo agregue al carrito mostrando un mensaje de que se agrego algo blabla.
    post = get_object_or_404(Post, pk=post_id)
    User = get_user_model()
    user = User.objects.get_or_create(username='usuario_anonimo')[0]

    carrito_item, created = CarritoItem.objects.get_or_create(
        post=post,
        usuario=user,
        precio_unitario=post.precio  # Asignar el precio del post al campo precio_unitario
    )

    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()

    return redirect('carrito')

def eliminar_del_carrito(request, carritoitem_id):
    carrito_item = get_object_or_404(CarritoItem, pk=carritoitem_id)
    carrito_item.delete()
    return redirect('carrito')


def vaciar_carrito(request):
    CarritoItem.objects.all().delete()
    return redirect('carrito')


def home(request):
    posts = Post.objects.filter(aprobado=True, relevante=True).order_by('-aprobado')
    
    # Obtener las categorías existentes
    categorias = Categoria.objects.all()
    
    # Obtener los usuarios existentes
    usuarios = User.objects.all()
    
    if request.user.is_authenticated:
        # Obtener el usuario actual
        user = request.user
        
        # Filtrar las publicaciones del usuario actual
        posts_by_user = posts.filter(user=user)
        
        # Obtener el conteo de publicaciones del usuario actual
        num_posts = posts_by_user.count()
        
        context = {
            'posts': posts,
            'num_posts': num_posts,
            'categorias': categorias,
            'usuarios': usuarios
        }
        return render(request, 'home.html', context)
    else:
        context = {
            'posts': posts,
            'categorias': categorias,
            'usuarios': usuarios
        }
        return render(request, 'home.html', context)

    
def contacto(request):
    if request.method == 'POST':

        return render(request, 'contacto.html', {
            
            'mensaje': 'Enviado Correctamente'
        }, print(request.POST))
    else:
        return render(request, 'contacto.html', {
            
        })

@login_required  
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
                return redirect('pending_posts')
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
    if user_passes_test(superuser_check):
        posts = Post.objects.filter(aprobado=False)
        return render(request, 'posts.html', {'posts': posts})
    else:
        posts = Post.objects.filter(aprobado=False, user=request.user)
        return render(request, 'posts.html', {'posts': posts})
    
def pending_posts(request):
    posts = Post.objects.filter(user=request.user, aprobado=False)
    return render(request, 'posts.html', {'posts': posts})

def posts_published(request):
    posts = Post.objects.filter(aprobado=True).order_by('-aprobado')
    return render(request, 'posts.html', {'posts': posts})

def post_por_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    productos = Post.objects.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'productos': productos
    }
    return render(request, 'post.html', context)

@login_required 
def create_post(request):
    if request.method == 'POST':
        try:
            form = PostForm(request.POST, request.FILES)  # Agregar request.FILES al inicializar el formulario
            if form.is_valid():
                if user_passes_test(superuser_check):
                    new_post = form.save(commit=False)
                    new_post.user = request.user
                    new_post.save()
                    print(request.POST, request.FILES)
                    return redirect('pending_posts')
        except ValueError:
            print(request.POST)
            return render(request, 'create_post.html', {
                'form': PostForm(),
                'error': 'Por favor, valide los datos'
            })
    else:
        return render(request, 'create_post.html', {
            'form': PostForm(),
        })

def post_detail(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
        return render(request, 'post_detail.html',{
            'post':post,
            'form': form
            })
    else:
        try:
            post = get_object_or_404(Post, pk=post_id)
            form = PostForm(request.POST, instance=post)
            form.save()
            return redirect('posts')
        except ValueError:
                return render(request, 'post_detail.html',{
                'post':post,
                'form': form,
                'error': 'Error al Actualizar'
                })
        
def detail(request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
        return render(request, 'detail.html',{
            'post':post,
            'form': form
            })

@login_required 
def published_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == 'POST':
        post.save()
        return redirect('home')
@login_required 
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
@login_required 
def signout(request):
    logout(request)
    CarritoItem.objects.all().delete()
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
            CarritoItem.objects.all().delete()
            return redirect('home')




# APLIQUÉ login_required y user_passes_test A LA VISTA DEL CARRITO
# PARA QUE EL USUARIO ACCEDA A LA VISTA SI NO ES ADMIN

# FUNCION PARA DETERMINAR SI EL USUARIO NO ES ADMIN
def no_es_admin(user):
    return not (user.is_superuser or user.is_staff)

# MODIFIQUÉ LA FUNCION PARA EVITAR QUE EL ADMIN ACCEDA AL CARRITO DE COMPRAS
def carrito(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'mensaje_admin.html')
    else:
        items = CarritoItem.objects.all()
        total_carrito = sum(item.subtotal() for item in items)
        return render(request, 'carrito.html', {'items': items, 'total_carrito': total_carrito})


def buscar(request):
    if request.method == 'GET':
        query = request.GET.get("q")

        #AL APRETAR BUSCAR (CON EL CAMPO VACÍO) MOSTRABA TODAS LAS OBRAS
        # CON ESTE CAMBIO MUESTRA EL MENSAJE DE "NO SE ENCONTRARON RESULTADOS"
        if not query:
            context = {'query': query}
            return render(request, 'resultado_busqueda.html', context)

        resultados = Post.objects.filter(
            Q(user__username__icontains=query) |  # Buscar por nombre de usuario del artista
            Q(titulo__icontains=query) |  # Buscar por título
            Q(id_categoria__categoria__icontains=query)  # Buscar por categoría
            #,imagen__isnull=False -- IGNORAR
        )

        context = {'resultados': resultados, 'query': query}
        return render(request, 'resultado_busqueda.html', context)
    
def post_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)
    productos_categoria = Post.objects.filter(id_categoria=categoria)

    context = {
        'categoria': categoria,
        'productos': productos_categoria
    }
    return render(request, 'productos_por.html', context)

def posts_por_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    productos_usuario = Post.objects.filter(user=usuario)

    context = {
        'usuario': usuario,
        'productos': productos_usuario
    }
    return render(request, 'productos_por.html', context)




#def productos_por_categoria(request, id_categoria):
    #categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    #productos = Post.objects.filter(id_categoria=categoria)
    #context = {
    #    'categoria': categoria,
    #    'productos': productos
    #}
    #return render(request, 'productos_por.html', context)


#def productos_por_usuario(request, username):

#    usuario = User.objects.get(username=username)

#    productos = Post.objects.filter(user=usuario)

 #   context = {
  #      'usuario': usuario,
   #     'productos': productos
 #  }
