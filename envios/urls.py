from django.urls import path

from . import views, views_cbv

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alias'),
    path('encomiendas/', views_cbv.EncomiendaListView.as_view(), name='encomienda_lista'),
    path('encomiendas/nueva/', views_cbv.EncomiendaCreateView.as_view(), name='encomienda_crear'),
    path('encomiendas/<int:pk>/', views_cbv.EncomiendaDetailView.as_view(), name='encomienda_detalle'),
    path('encomiendas/<int:pk>/editar/', views_cbv.EncomiendaUpdateView.as_view(), name='encomienda_editar'),
]
