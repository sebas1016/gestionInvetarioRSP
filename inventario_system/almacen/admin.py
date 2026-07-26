from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(TipoRepuesto)
admin.site.register(Anaquel)
admin.site.register(Repuesto)
admin.site.register(MovimientoInventario)

@admin.register(UnidadRepuesto)
class UnidadAdmin(admin.ModelAdmin):

    list_display=[
        'codigo_unico',
        'repuesto',
        'estado',
        'anaquel'
    ]

    exclude=[
        'codigo_unico',
        'codigo_barras',
        'qr'
    ]

@admin.register(BoardRegistroFotografico)
class FotoAdmin(admin.ModelAdmin):

    list_display=[
        'unidad',
        'version',
        'fecha'
    ]

    readonly_fields=[
        'version'
    ]


@admin.register(ComponenteRetirado)
class ComponenteAdmin(admin.ModelAdmin):

    list_display=[
        'unidad',
        'referencia',
        'nombre',
        'fecha'
    ]