# Importamos settings para poder tener a la mano la ruta de la carpeta media
import datetime
import json

from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView

from .get_username import get_username
from .models import PagoInscCuota, Inscripcion, Alumno, Caja, Concepto, PagoInscCuotaSocio
from gestionAlumnos.models import PeriodoCurso
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

class AlumnoDeleteView(DeleteView):
    model = Alumno
    success_url = reverse_lazy('admin/gestionAlumnos')
   
    success_message = "Session %(nombre)s was removed successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(AlumnoDeleteView, self).delete(request, *args, **kwargs)

    
def index(request):
    return render(request, "index.html", {})


def pagoInscCuota(request):
    return render_to_response(
        "admin/pagoInscCuota/add.html",
        {'title': 'Pago de cuota de los alumnos'},
        RequestContext(request, {}),
    )   
def pagoInscCuotaSocio(request):
    return render_to_response(
        "admin/pagoInscCuotaSocio/add.html",
        {'title': 'Pago de cuota de los Socios'},
        RequestContext(request, {}),
    )  
    
def modificarinsccuota(request):
    return render_to_response(
        "admin/pagoInscCuota/modificar.html",
        {'title': 'Modificar cuota de los alumnos'},
        RequestContext(request, {}),
    )   

def modificarinsccuotasocio(request):
    return render_to_response(
        "admin/pagoInscCuotaSocio/modificar.html",
        {'title': 'Modificar cuota de los Socios'},
        RequestContext(request, {}),
    )
    

def inscripcionMasiva(request):
    return render_to_response(
        "admin/InscripcionMasiva/AddInscripcionMasiva.html",
        {'title': 'Inscripcion Masiva de alumnos'},
        RequestContext(request, {}),
    )   

@csrf_exempt  # POST security    
def inscripcionMasivaCarga(request):
    alumnosDesde = [];   
    if request.POST['id_periodo_origen'] != '' and request.POST['id_periodo_destino'] != '':
        sql = ""   
        sql += " select distinct a.dni, a.apellido, a.nombre "
        sql += " from inscripcion i "
        sql += "     inner join periodo_curso p on p.id_periodo_curso = i.id_periodo_curso "
        sql += "     inner join alumno a on a.id_alumno = i.id_alumno "
        sql += "     LEFT JOIN ( "
        sql += "         select a_aux.dni "
        sql += "         from inscripcion i_aux  "     
        sql += "         inner join periodo_curso p_aux on p_aux.id_periodo_curso = i_aux.id_periodo_curso   "    
        sql += "         inner join alumno a_aux on a_aux.id_alumno = i_aux.id_alumno "
        sql += "         where  p_aux.id_periodo_curso = " + request.POST['id_periodo_destino']
        sql += "     ) alum on alum.dni = a.dni "
        sql += " where alum.dni is null and p.id_periodo_curso = " + request.POST['id_periodo_origen']                   
        print(sql) 
        
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows = cursor.fetchall()           
            
        for row in rows:
            alumno = {}
            alumno["dni"] = row[0]
            alumno["apellido"] = row[1]
            alumno["nombre"] = row[2]
            alumnosDesde.append(alumno)  
        cursor.close()
               
    else:
        return JsonResponse()    
    return JsonResponse({"alumnosDesde": alumnosDesde})   

@csrf_exempt  # POST security    
def inscripcionMasivaSave(request):
    if request.is_ajax():               
        if request.POST['id_periodo_destino'] != '':
            alumnos = request.POST.getlist('alumnos[]')   
            print("id_periodo_destino: " + request.POST['id_periodo_destino'])       
            periodo = PeriodoCurso.objects.get(id_periodo_curso=request.POST['id_periodo_destino'])                            
            for row in alumnos:                                   
                print(str(row))         
                inscripcion = Inscripcion()               
                inscripcion.id_alumno = Alumno.objects.get(dni=row)
                inscripcion.id_periodo_curso=periodo
                inscripcion.fecha_alta = datetime
                inscripcion.estado = 'Inscripto'
                inscripcion.save()                             
    return HttpResponse("OK")
    
@csrf_exempt  # POST security
def get_cuotas_a_pagar(request): 
    cuotas = []; 
    if request.POST['id_inscripcion'] != '':
        sql = ""   
        sql += " select p.fecha_inicio, p.cant_meses "
        sql += " from inscripcion i "
        sql += "     inner join periodo_curso p on p.id_periodo_curso = i.id_periodo_curso "
        sql += " where id_inscripcion = " + request.POST['id_inscripcion'];    
        print(sql) 
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows = cursor.fetchall()           
    
        cant_meses = 0
        for row in rows:
            fecha_alta = row[0]
            cant_meses = row[1]  
        cursor.close()
                       
        mesInicio = fecha_alta.strftime("%m")
        anoInicio = fecha_alta.strftime("%Y")
        for x in range(0, cant_meses):           
            cuota = [x , (str(int(mesInicio) + x).rjust(2, '0') + "/" + anoInicio)]  
            cursor = connection.cursor()
            sql = "select id_pago_insc_cuota from pago_insc_cuota where id_inscripcion = " + request.POST['id_inscripcion'] + " and fecha_cuota like '" + anoInicio + "-" + str(int(mesInicio) + x).rjust(2, '0') + "-01'"
            print(sql)
            cursor.execute(sql) 
            if cursor.rowcount == 0:
                cuotas.append(cuota)                                 
            cursor.close()        
            
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(cuotas)))

@csrf_exempt  # POST security
def get_cuotas_socios_a_pagar(request): 
    cuotas = []; 
    if request.POST['id_alumno'] != '':
        for x in range(0, 4):           
            cursor = connection.cursor()
            sql = "select id_pago_insc_cuota_soc "
            sql += "from pago_insc_cuota_socio "
            sql += "where id_alumno = " + request.POST['id_alumno']
            sql += " and nro_cuota = " + str(x+1)

            cursor.execute(sql) 
            if cursor.rowcount == 0:
                cuota = [(x+1) , 'Cuota ' + str(x+1)]
                cuotas.append(cuota)                                 
            cursor.close()        
            
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(cuotas)))

@csrf_exempt  # POST security
def get_cuotas_socios_pagas(request): 
    cuotas = []; 
    if request.POST['id_alumno'] != '':
        cursor = connection.cursor()
        sql = "select id_pago_insc_cuota_soc, nro_cuota "
        sql += "from pago_insc_cuota_socio "
        sql += "where id_alumno = " + request.POST['id_alumno']
        sql += " order by nro_cuota asc"
        cursor.execute(sql) 
        rows = cursor.fetchall()        
        for row in rows:            
            cuota = [row[0] , 'Cuota ' + str(row[1])]
            cuotas.append(cuota)                                
        cursor.close()           
            
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(cuotas)))    

@csrf_exempt  # POST security
def get_cuotas_pagas(request): 
    cuotas = []; 
    if request.POST['id_inscripcion'] != '':
        sql = ""   
        sql += " select pic.id_pago_insc_cuota, DATE_FORMAT(pic.fecha_cuota, '%m/%Y') "
        sql += " from pago_insc_cuota pic "
        sql += " where pic.id_inscripcion = " + request.POST['id_inscripcion'];    
        print(sql) 
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows = cursor.fetchall()           
    
        for row in rows:
            cuota = [row[0] , str(row[1])]
            cuotas.append(cuota) 
        cursor.close()
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(cuotas)))
    

@csrf_exempt  # POST security
def save_insc_cuota(request):   
    if request.POST['id_inscripcion'] != '' and request.POST['fecha_cuota'] != '' and request.POST['importe'] != '':
        inscripcion = Inscripcion.objects.get(id_inscripcion=request.POST['id_inscripcion'])            
                         
        pagoInscCuota = PagoInscCuota()           
        pagoInscCuota.fecha_alta = datetime.datetime.now()
        pagoInscCuota.id_inscripcion = inscripcion
        pagoInscCuota.fecha_cuota = datetime.datetime.strptime("01/" + str(request.POST['fecha_cuota']), "%d/%m/%Y").date()
        pagoInscCuota.fecha_pago = datetime.datetime.now()      
        pagoInscCuota.importe = request.POST['importe']
        pagoInscCuota.usuario = str(get_username()) 
        pagoInscCuota.pagado = True 
        pagoInscCuota.es_socio = False     
        pagoInscCuota.save()  
        response = HttpResponse()
        response.write(str(pagoInscCuota.id_pago_insc_cuota))
    # for row in rows    
    return response

@csrf_exempt  # POST security
def save_insc_cuota_socio(request):   
    if request.POST['id_alumno'] != '' and request.POST['nro_cuota'] != '' and request.POST['importe'] != '':
        alumno = Alumno.objects.get(id_alumno=request.POST['id_alumno'])            
                         
        pagoInscCuota = PagoInscCuotaSocio() 
        pagoInscCuota.id_alumno = alumno
        pagoInscCuota.fecha_alta = datetime.datetime.now()
        pagoInscCuota.nro_cuota = request.POST['nro_cuota']
        pagoInscCuota.fecha_pago = datetime.datetime.now()      
        pagoInscCuota.importe = request.POST['importe']
        pagoInscCuota.usuario = str(get_username())         
        pagoInscCuota.save()  
        response = HttpResponse()
        response.write(str(pagoInscCuota.id_pago_insc_cuota_soc))
    # for row in rows    
    return response


@csrf_exempt  # POST security
def update_insc_cuota(request):   
    if request.POST['cbxCuota'] != '' and request.POST['importe'] != '':
        cursor = connection.cursor()
        cursor.execute("update pago_insc_cuota set importe = " + request.POST['importe'] + " where id_pago_insc_cuota = " + request.POST['cbxCuota'])   
        cursor.close()                    
    return HttpResponse()

@csrf_exempt  # POST security
def delete_insc_cuota(request):   
    if request.POST['cbxCuota'] != '':
        pagoInscCuota = PagoInscCuota.objects.get(id_pago_insc_cuota=request.POST['cbxCuota'])        
        pagoInscCuota.delete()        
    # for row in rows    
    return HttpResponse()


@csrf_exempt  # POST security
def update_socio_cuota(request):   
    if request.POST['nro_cuota'] != '' and request.POST['importe'] != '':
        cursor = connection.cursor()
        cursor.execute("update pago_insc_cuota_socio set importe = " + request.POST['importe'] + " where id_pago_insc_cuota_soc = " + request.POST['nro_cuota'])   
        cursor.close()                    
    return HttpResponse()

@csrf_exempt  # POST security
def delete_socio_cuota(request):   
    if request.POST['nro_cuota'] != '':
        pagoInscCuota = PagoInscCuotaSocio.objects.get(id_pago_insc_cuota_soc=request.POST['nro_cuota'])        
        pagoInscCuota.delete()        
    # for row in rows    
    return HttpResponse()


@csrf_exempt  # POST security
def get_importe_inscripcion(request):
    if request.POST['id_inscripcion'] != '':
        sql = ""
        sql += " select pc.importe " 
        sql += " from inscripcion i " 
        sql += " inner join periodo_curso pc on pc.id_periodo_curso = i.id_periodo_curso "
        sql += " where i.id_inscripcion = " + request.POST['id_inscripcion']
        print(sql) 
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows = cursor.fetchall()   
        cursor.close()
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(rows)))

@csrf_exempt  # POST security
def get_importe_socio(request):   
    sql = ""
    sql += " select (case when c.importe_socio is null then 0 else c.importe_socio end) as importe " 
    sql += " from configuracion c " 
    sql += " limit 1"
    print(sql) 
    cursor = connection.cursor()
    cursor.execute(sql) 
    rows = cursor.fetchall()   
    cursor.close()
   
    # for row in rows    
    return JsonResponse(dict(genres=list(rows)))

@csrf_exempt  # POST security
def get_importe_inscripcion_pagado(request):
    if request.POST['cbxCuota'] != '':
        sql = ""
        sql += " select pic.importe "
        sql += " from pago_insc_cuota pic "
        sql += " where pic.id_pago_insc_cuota = " + request.POST['cbxCuota']
        print(sql) 
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows = cursor.fetchall()   
        cursor.close()
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(rows)))


@csrf_exempt  # POST security
def get_importe_socio_pagado(request):
    if request.POST['nro_cuota'] != '':
        sql = ""
        sql += " select pic.importe "
        sql += " from pago_insc_cuota_socio pic "
        sql += " where pic.id_pago_insc_cuota_soc = " + request.POST['nro_cuota']
        print(sql) 
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows = cursor.fetchall()   
        cursor.close()
    else:
        return JsonResponse()
    # for row in rows    
    return JsonResponse(dict(genres=list(rows)))
