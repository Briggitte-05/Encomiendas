from django.db import models
from django.utils import timezone

class EncomiendaQuerySet(models.QuerySet):
    # --- Filtros por estado ---
    def pendientes(self):
        return self.filter(estado='PE')

    def en_transito(self):
        return self.filter(estado='TR')

    def entregadas(self):
        return self.filter(estado='EN')

    def activas(self):
        """Pendientes + en tránsito + en destino"""
        return self.filter(estado__in=['PE', 'TR', 'DE'])

    # --- Filtros compuestos ---
    def por_ruta(self, ruta):
        return self.filter(ruta=ruta)

    def con_retraso(self):
        """Encomiendas activas cuya fecha estimada ya pasó"""
        return self.activas().filter(
            fecha_entrega_est__lt=timezone.now().date()
        )

    # --- Optimización (Evita que el sistema sea lento) ---
    def con_relaciones(self):
        """Trae de un solo golpe los datos de clientes y rutas"""
        return self.select_related(
            'remitente', 'destinatario', 'ruta', 'empleado_registro'
        )

class ClienteQuerySet(models.Model): # Nota: Aquí la guía lo usa como base
    pass

# Implementación rápida para que funcionen los managers:
class ClienteQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(estado=1)

    def buscar(self, termino):
        return self.filter(
            models.Q(nombres__icontains=termino) | 
            models.Q(apellidos__icontains=termino) | 
            models.Q(nro_doc__icontains=termino)
        )

class RutaQuerySet(models.QuerySet):
    def activas(self):
        return self.filter(estado=1)