# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from envios import views, views_auth
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('envios.urls')),  # Conecta las URLs de tu app envios
    path('accounts/login/', views_auth.login_view),
    path('accounts/logout/', views_auth.logout_view),
    path('accounts/', include('django.contrib.auth.urls')), # URLs para login/logout
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('perfil/', views_auth.perfil_view, name='perfil'),
]

# Configuración para servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = 'Sistema de Gestión de Encomiendas' # Título en la barra azul arriba
admin.site.site_title  = 'Encomiendas Admin'                # Título en la pestaña del navegador
admin.site.index_title = 'Panel de Administración'           # Subtítulo en la página de inicio del admin
