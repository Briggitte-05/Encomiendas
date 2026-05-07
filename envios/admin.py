# envios/admin.py 
from django.contrib import admin 
from django.utils.html import format_html 
from .models import Empleado, Encomienda, HistorialEstado 

@admin.register(Encomienda) 
class EncomiendaAdmin(admin.ModelAdmin): 
    # 1. Columnas visibles
    list_display = ('codigo', 'remitente_nombre', 'destinatario_nombre', 
                    'ruta', 'estado_badge', 'peso_kg', 'fecha_registro') 
    
    # 2. Filtros 
    list_filter = ('estado', 'ruta', 'fecha_registro') 
    
    # 3. Buscador
    search_fields = ('codigo', 'remitente__apellidos', 'destinatario__apellidos', 'remitente__nro_doc') 
    
    # 4. campos por solo lectura (no editables)
    readonly_fields = ('codigo', 'fecha_registro', 'fecha_entrega_real') 
    
    ordering = ('-fecha_registro',) 
    list_per_page = 20 

    # 5. Organización del formulario por secciones (Fieldsets)
    fieldsets = ( 
        ('Identificación', { 
            'fields': ('codigo', 'descripcion', 'peso_kg', 'volumen_cm3') 
        }), 
        ('Partes involucradas', { 
            'fields': ('remitente', 'destinatario', 'ruta', 'empleado_registro') 
        }), 
        ('Estado y Tiempos', { 
            'fields': ('estado', 'costo_envio', 'fecha_registro', 'fecha_entrega_est', 'fecha_entrega_real') 
        }), 
        ('Información Adicional', { 
            'classes': ('collapse',),  # Esta sección aparece cerrada por defecto
            'fields': ('observaciones',) 
        }), 
    ) 

    # Métodos para mostrar nombres completos en la lista
    def remitente_nombre(self, obj): 
        return f"{obj.remitente.nombres} {obj.remitente.apellidos}" 
    remitente_nombre.short_description = 'Remitente' 

    def destinatario_nombre(self, obj): 
        return f"{obj.destinatario.nombres} {obj.destinatario.apellidos}" 
    destinatario_nombre.short_description = 'Destinatario' 

    # Círculos de colores para el estado (HTML en el Admin)
    def estado_badge(self, obj): 
        colores = { 
            'PE': '#6c757d',   # gris
            'TR': '#0d6efd',   # azul
            'DE': '#fd7e14',   # naranja
            'EN': '#198754',   # verde
            'DV': '#dc3545',   # rojo
        } 
        color = colores.get(obj.estado, '#6c757d') 
        return format_html( 
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>', 
            color, obj.get_estado_display() 
        ) 
    estado_badge.short_description = 'Estado' 

@admin.register(Empleado) 
class EmpleadoAdmin(admin.ModelAdmin): 
    list_display = ('codigo', 'apellidos', 'nombres', 'cargo', 'email', 'estado') 
    list_filter = ('cargo', 'estado') 
    search_fields = ('codigo', 'apellidos', 'nombres', 'email') 

@admin.register(HistorialEstado) 
class HistorialEstadoAdmin(admin.ModelAdmin): 
    list_display = ('encomienda', 'estado_anterior', 'estado_nuevo', 'empleado', 'fecha_cambio') 
    readonly_fields = ('encomienda', 'estado_anterior', 'estado_nuevo', 'empleado', 'fecha_cambio') 
    list_filter = ('estado_nuevo',) 
    ordering = ('-fecha_cambio',)
