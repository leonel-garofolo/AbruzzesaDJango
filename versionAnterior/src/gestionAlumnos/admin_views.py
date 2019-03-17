from .models import Alumno
from django.contrib import admin
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def informe_alumno_cuotas(request):
    return render_to_response(
        "admin/alumnos/informe_alumno_cuotas.html",
        {'title': 'Listado de Alumnos Cuotas Pagadas'},
        RequestContext(request, {}),
    )
report_alumno = staff_member_required(informe_alumno_cuotas)
admin.site.register_view('gestionAlumnos/informe_alumno_cuotas/', 'Informe Alumnos Cuotas', view=report_alumno)

@staff_member_required
def informe_alumno_inscriptos(request):
    return render_to_response(
        "admin/alumnos/informe_alumno_inscriptos.html",
        {'title': 'Listado de Alumnos Inscriptos'},
        RequestContext(request, {}),
    )
report_alumno = staff_member_required(informe_alumno_inscriptos)
admin.site.register_view('gestionAlumnos/informe_alumno/', 'Informe Alumnos Inscriptos', view=report_alumno)

@staff_member_required
def informe_alumno_moroso(request):
    return render_to_response(
        "admin/alumnos/informe_alumno_moroso.html",
        {'title': 'Listado de Alumnos Morosos'},
        RequestContext(request, {}),
    )
report_alumno_moroso = staff_member_required(informe_alumno_moroso)
admin.site.register_view('gestionAlumnos/informe_alumno_moroso/', 'Informe Alumnos Morosos', view=report_alumno_moroso)

@staff_member_required
def informe_balance(request):
    return render_to_response(
        "admin/alumnos/informe_balance.html",
        {'title': 'Listado de Balance'},
        RequestContext(request, {}),
    )
report_balance = staff_member_required(informe_balance)
admin.site.register_view('gestionAlumnos/informe_balance/', 'Informe Balance', view=informe_balance)