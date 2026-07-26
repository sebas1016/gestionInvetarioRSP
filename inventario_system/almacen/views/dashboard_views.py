from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..services.dashboard_service import DashboardService



def dashboard(request):
    context = {"resumen": DashboardService.obtener_resumen()}
    return render(request, "dashboard/dashboard.html", context)