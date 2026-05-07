# envios/views.py 
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.utils import timezone 

# Importamos los modelos necesarios
from .models import Encomienda, Empleado, HistorialEstado 
from clientes.models import Cliente 
from rutas.models import Ruta 
from config.choices import EstadoEnvio 
from django.http import JsonResponse, Http404

from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator


def es_empleado_activo(user): 
    """Esta función verifica si el usuario es un trabajador habilitado"""
    return ( 
        user.is_authenticated and 
        Empleado.objects.filter(email=user.email, estado=1).exists() 
    )
    
# ── Vista real: dashboard del sistema ──────────────────────── 
@login_required 
def dashboard(request): 
    """Vista principal del sistema con estadísticas""" 
    hoy = timezone.now().date() 
    
    # El diccionario context envía los datos a dashboard.html
    context = { 
        'total_activas':   Encomienda.objects.activas().count(), 
        'en_transito':     Encomienda.objects.en_transito().count(), 
        'con_retraso':     Encomienda.objects.con_retraso().count(), 
        'entregadas_hoy':  Encomienda.objects.filter( 
                                estado=EstadoEnvio.ENTREGADO, 
                                fecha_entrega_real=hoy
                           ).count(), 
        'ultimas':         Encomienda.objects.con_relaciones()[:5], 
    } 
    
    return render(request, 'envios/dashboard.html', context)

# ── Vista: Lista de Encomiendas ──────────────────────────────
@require_GET
@login_required
def encomienda_lista(request): 
    qs = Encomienda.objects.con_relaciones() 
    
    estado = request.GET.get('estado', '') 
    q      = request.GET.get('q', '') 
    
    if estado: 
        qs = qs.filter(estado=estado) 
    if q: 
        from django.db.models import Q 
        qs = qs.filter( 
            Q(codigo__icontains=q) | 
            Q(remitente__apellidos__icontains=q) | 
            Q(destinatario__apellidos__icontains=q) 
        ) 
    
    paginator   = Paginator(qs, 15)           
    page_number = request.GET.get('page', 1)  
    encomiendas = paginator.get_page(page_number) 
    
    return render(request, 'envios/lista.html', { 
        'encomiendas':   encomiendas,   # Ahora enviamos el objeto paginado
        'estados':       EstadoEnvio.choices, 
        'estado_activo': estado, 
        'q':             q, 
    })
    
# ── Vista: Detalle de una Encomienda ─────────────────────────
@login_required
def encomienda_detalle(request, pk):
    """Muestra la información completa de una sola encomienda"""
    # Usamos el atajo get_object_or_404 que aprendimos
    encomienda = get_object_or_404(Encomienda.objects.con_relaciones(), pk=pk)
    
    return render(request, 'envios/detalle.html', {
        'encomienda': encomienda
    })
    
# ── Vista: Crear una Nueva Encomienda ────────────────────────
@user_passes_test(es_empleado_activo, login_url='/sin-permiso/') # <--- Agregamos esto
@permission_required('envios.add_encomienda', raise_exception=True)
@require_http_methods(['GET', 'POST'])
@login_required 
def encomienda_crear(request): 
    from .forms import EncomiendaForm 
     
    if request.method == 'POST': 
        form = EncomiendaForm(request.POST) 
        if form.is_valid(): 
            enc = form.save(commit=False) 
            
            try:
                # Cambiamos a buscar por 'user' para que coincida con tu modelo
                enc.empleado_registro = Empleado.objects.get(user=request.user)
            except Empleado.DoesNotExist:
                messages.error(request, "Tu usuario no tiene un perfil de Empleado asociado.")
                return redirect('dashboard')

            enc.save() 
            messages.success(request, f'Encomienda {enc.codigo} registrada correctamente.') 
            return redirect('encomienda_detalle', pk=enc.pk) 
    else: 
        form = EncomiendaForm() 
    
    return render(request, 'envios/form.html', { 'form': form, 'titulo': 'Nueva Encomienda' })

# ── Vista: Cambiar el estado de una Encomienda ─────────────────
@require_POST
@login_required 
def encomienda_cambiar_estado(request, pk): 
    enc = get_object_or_404(Encomienda, pk=pk) 
    
    if request.method == 'POST': 
        nuevo_estado = request.POST.get('estado') 
        observacion  = request.POST.get('observacion', '') 
        
        try: 
            # Cambiamos aquí también para ser consistentes
            empleado = Empleado.objects.get(user=request.user) 
            enc.cambiar_estado(nuevo_estado, empleado, observacion) 
            messages.success(request, f'Estado actualizado a: {enc.get_estado_display()}') 
        except (Empleado.DoesNotExist, ValueError) as e: 
            messages.error(request, f'Error: {str(e)}') 
            
    return redirect('encomienda_detalle', pk=pk)


def encomienda_estado_json(request, pk): 
    enc = get_object_or_404(Encomienda, pk=pk) 
    return JsonResponse({ 
        'codigo':  enc.codigo, 
        'estado':  enc.estado, 
        'display': enc.get_estado_display(),
    })
    

@login_required
def eliminar_encomienda(request, pk): 
    enc = get_object_or_404(Encomienda, pk=pk) 
    
    # Lógica de seguridad: solo se borra si no ha salido a ruta
    if enc.estado != 'PE': 
        messages.error(request, 'No puedes eliminar una encomienda que ya no está pendiente.')
        raise PermissionDenied   
        
    if request.method == 'POST': 
        enc.delete() 
        messages.success(request, 'Encomienda eliminada correctamente.') 
        return redirect('encomienda_lista') 
        
    return render(request, 'envios/confirmar_eliminar.html', {'enc': enc})