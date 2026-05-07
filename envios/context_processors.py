# envios/context_processors.py
from .models import Encomienda

def estadisticas_globales(request):
    """
    Inyecta datos en el navbar de todas las páginas automáticamente.
    """
    # Si el usuario no ha iniciado sesión, no calculamos nada
    if not request.user.is_authenticated:
        return {}

    # Devolvemos los conteos que queremos ver en el menú
    return {
        'nav_activas': Encomienda.objects.activas().count(),
        'nav_retraso': Encomienda.objects.con_retraso().count(),
        'nav_pendientes': Encomienda.objects.pendientes().count(),
    }