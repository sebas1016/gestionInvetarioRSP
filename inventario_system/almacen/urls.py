from django.urls import path
from .views import dashboard_views
from .views.inventario_views import *
from .views.repuesto_views import *
from .views import historial_views
from .views.historial_views import *
from .views.unidad_views import *
from .views.configuracion_views import *
from .views.crear_views import *
from .views.editar_views import *
from .views.eliminar_views import *
from .views import *
urlpatterns=[

    # almacen/urls.py
    path("", dashboard_views.dashboard, name="dashboard"),
    path("unidades/<int:pk>/", historial_views.unidad_detail, name="unidad_detail"),
    # almacen/urls.py
    path("ingreso/",ingreso_repuesto, name="ingreso_repuesto"),
    path("repuestos/", repuesto_list, name="repuesto_list"),
    path("repuestos/<int:pk>/", repuesto_detail, name="repuesto_detail"),
    #--Configuracion
    path("marcas/", configuracion_views.marca_list, name="marca_list"),
    path("marcas/<int:pk>/editar/", configuracion_views.marca_edit, name="marca_edit"),
    path("marcas/<int:pk>/eliminar/", configuracion_views.marca_delete, name="marca_delete"),

    path("modelos/", configuracion_views.modelo_list, name="modelo_list"),
    path("modelos/<int:pk>/editar/", configuracion_views.modelo_edit, name="modelo_edit"),
    path("modelos/<int:pk>/eliminar/", configuracion_views.modelo_delete, name="modelo_delete"),

    path("tipos/", configuracion_views.tipo_list, name="tipo_list"),
    path("tipos/<int:pk>/editar/", configuracion_views.tipo_edit, name="tipo_edit"),
    path("tipos/<int:pk>/eliminar/", configuracion_views.tipo_delete, name="tipo_delete"),

    path("anaqueles/", configuracion_views.anaquel_list, name="anaquel_list"),
    path("anaqueles/<int:pk>/editar/", configuracion_views.anaquel_edit, name="anaquel_edit"),
    path("anaqueles/<int:pk>/eliminar/", configuracion_views.anaquel_delete, name="anaquel_delete"),
    
    #--Repuesto CRUD
    path("repuestos/nuevo/", inventario_views.repuesto_create, name="repuesto_create"),
    path("repuestos/<int:pk>/editar/", inventario_views.repuesto_edit, name="repuesto_edit"),
    path("repuestos/<int:pk>/eliminar/", inventario_views.repuesto_delete, name="repuesto_delete"),
    
    #--BarCode
    path("unidades/<int:pk>/etiqueta/", historial_views.unidad_etiqueta, name="unidad_etiqueta"),
    path("repuestos/<int:pk>/etiqueta/", historial_views.repuesto_etiqueta, name="repuesto_etiqueta"),
    
    #Buscar por codigo de barras
    path("buscar/", inventario_views.buscar_por_codigo, name="buscar_codigo"),
    
    #SAlidas
    path("salida/", movimiento_views.salida, name="salida"),
    
    #Historial movimientos
    path("movimientos/", movimiento_views.movimiento_list, name="movimiento_list"),
]