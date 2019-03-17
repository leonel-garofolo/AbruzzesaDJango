from django.conf.urls import url
from . import admin_views
from . import views
from . import reports
from . import explorers
urlpatterns = [    
    #generador de reporte
    url(r'^admin/gestionAlumnos/generar_reporte$', reports.generar_reporte, name='generar_reporte'),
    url(r'^admin/gestionAlumnos/generar_reporte_csv$', reports.generar_reporte_csv, name='generar_reporte_csv'),
    url(r'^admin/gestionAlumnos/pagoinsccuota/$', views.pagoInscCuota, name='pagoInscCuota'),
    url(r'^admin/gestionAlumnos/modificarinscripcion/$', views.modificarinsccuota, name='modificarinsccuota'),
    
    #inscripcion masiva de alumnos
    url(r'^admin/gestionAlumnos/inscripcion/$', views.inscripcionMasiva, name='inscripcionMasiva'),
    url(r'^admin/gestionAlumnos/inscripcion/cargar$', views.inscripcionMasivaCarga, name='inscripcionMasivaCarga'),
    url(r'^admin/gestionAlumnos/inscripcion/save$', views.inscripcionMasivaSave, name='inscripcionMasivaSave'),
    

    #alumno
   #url(r'^admin/gestionAlumnos/alumno/add/$', views.AlumnoDeleteView.as_view(), name='alumno-delete'),
    #Exploradores
    url(r'^admin/explorer/e_curso$', explorers.e_curso, name='e_curso'),
    url(r'^admin/explorer/e_idioma$', explorers.e_idioma, name='e_idioma'),
    url(r'^admin/explorer/e_periodo$', explorers.e_periodo, name='e_period'),
    url(r'^admin/explorer/e_periodo_anterior$', explorers.e_periodo_anterior, name='e_periodo_anterior'),
     url(r'^admin/explorer/e_periodo_posterior$', explorers.e_periodo_posterior, name='e_periodo_posterior'),
    url(r'^admin/explorer/e_alumno$', explorers.e_alumno, name='e_alumno'),
    url(r'^admin/explorer/e_concepto$', explorers.e_concepto, name='e_concepto$'),
    url(r'^admin/explorer/e_inscripcion$', explorers.e_inscripcion, name='e_inscripcion$'),
    
    #Funciones    
    url(r'^admin/function/get_meses_cuotas$', views.get_cuotas_a_pagar, name='get_cuotas_a_pagar'),
     url(r'^admin/function/get_cuotas_pagas$', views.get_cuotas_pagas, name='get_cuotas_pagas'),
     
    url(r'^admin/function/save_insc_cuota$', views.save_insc_cuota, name='save_insc_cuota'),
    url(r'^admin/function/ticket$', reports.ticket, name='ticket'),
    url(r'^admin/function/update_insc_cuota$', views.update_insc_cuota, name='update_insc_cuota'),
    url(r'^admin/function/delete_insc_cuota$', views.delete_insc_cuota, name='delete_insc_cuota'),
    
    url(r'^admin/function/get_importe_inscripcion$', views.get_importe_inscripcion, name='get_importe_inscripcion'),
    url(r'^admin/function/get_importe_inscripcion_pagado$', views.get_importe_inscripcion_pagado, name='get_importe_inscripcion_pagado'),            
]
