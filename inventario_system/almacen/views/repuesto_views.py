from django.shortcuts import render
from ..models.repuesto import Repuesto
from django.db.models import Q
from core.utils.page import page_context

def lista_repuestos(request):

    busqueda=request.GET.get(
        'buscar',
        ''
    )

    repuestos = (
    Repuesto.objects
    .select_related(
        'modelo__marca',
        'modelo'
    )
)

    if busqueda:

        repuestos=repuestos.filter(
            Q(referencia__icontains=busqueda) |

            Q(modelo__nombre__icontains=busqueda) |

            Q(modelo__marca__nombre__icontains=busqueda) |

            Q(tipo__nombre__icontains=busqueda)
        )

    contexto=page_context(
        title='Repuestos',  
        description='administración de repuestos',
        breadcrumbs=[

            {
                'title':'Inicio',
                'url':'dashboard'
            },
            {
                'title':'Repuestos',
                'url':None
            }
        ],
        action={
            'title':'Nuevo repuesto',
           # 'url':'inventario:crear',
            'icon':'bi-plus-circle'
        },
        
        repuestos=repuestos

    )

    return render(
        request,
        'inventario/lista_repuestos.html',
        contexto
    )