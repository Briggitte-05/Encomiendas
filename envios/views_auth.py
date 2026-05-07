# envios/views_auth.py
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm 

def login_view(request): 
    """Vista para el login de empleados""" 
    # 1. Si el usuario ya entró, no le muestres el login, mándalo al dashboard
    if request.user.is_authenticated: 
        return redirect('dashboard') 

    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password') 
            user = authenticate(username=username, password=password) 
            
            if user is not None: 
                login(request, user) 
                messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}!') 
                
                # 'next' sirve para que si el usuario quería ir a una página específica, 
                # el sistema lo mande ahí después de loguearse.
                next_page = request.GET.get('next', 'dashboard') 
                return redirect(next_page) 
            else: 
                messages.error(request, 'Usuario o contraseña incorrectos.') 
        else: 
            messages.error(request, 'Por favor corrige los errores del formulario.') 
    else: 
        form = AuthenticationForm() 
    
    return render(request, 'accounts/login.html', {'form': form}) 

def logout_view(request): 
    """Cierra la sesión del usuario""" 
    logout(request) 
    messages.info(request, 'Has cerrado sesión correctamente.') 
    return redirect('login') 

@login_required 
def perfil_view(request): 
    """Muestra los datos del empleado logueado""" 
    return render(request, 'accounts/perfil.html', {'user': request.user})