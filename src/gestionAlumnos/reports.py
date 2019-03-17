import  csv
from time import gmtime, strftime
from io import BytesIO
import datetime
from django.db import connection
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, A5, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import  Paragraph, TableStyle
from reportlab.platypus import Table
from .report_util import _page_properties, NumberedCanvas
from .utils import sqlDateFormat
from reportlab.lib.units import inch

class Report:
    posicion = A4
    titulo = ""
    list_style = TableStyle(
        [
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.lightblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue)
        ]
    )
    cantidad = ""  
    total = "" 
    
class ReportCSV:
    titulo = ""
    

def generar_reporte(request):
    reporte = Report()
    sReportName = request.GET['report_name']
    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()         
    sql = getQueryReport(request, sReportName, reporte)
    
    doc = _page_properties(sReportName, buff, reporte.posicion,40,40,60,18)  
    builder = []
    styles = getSampleStyleSheet()
    header = Paragraph(reporte.titulo, styles['Heading1'])   
    builder.append(header)
       
    # Data retrieval operation - no commit required
    cursor = connection.cursor()
    cursor.execute(sql)   
    cursor.close()
    
    if reporte.cantidad != '':
        builder.append(Paragraph(reporte.cantidad + " " + str(cursor.rowcount), styles['Heading4']) )      
    if reporte.total != '':
        builder.append(Paragraph("Total Importe de Ingresos: " + reporte.total + "$", styles['Heading4']) )        
    
    headings = [i[0] for i in cursor.description]
    data = list(cursor)
            
    t = Table([headings] + data )        
    t.setStyle(reporte.list_style)
    builder.append(t)
    doc.build(builder, canvasmaker=NumberedCanvas)
    response.write(buff.getvalue())
    buff.close()
    return response

def getQueryReport(request, reportName, reporte):
    sql = ""
    if reportName == "alumnosInscriptos":
        reporte.titulo = "Listado de Alumnos Inscriptos"
        reporte.cantidad = "Cantidad de Inscriptos: "
        sql = sqlAlumnosInscriptos(request)       
    if reportName == "ImporteAlumnosInscriptos":
        reporte.titulo = "Cantidad de Alumnos Inscriptos"
        sql = sqlAlumnosImporte(request)
    if reportName == "alumnosCuotas":        
        genericStyle(reporte)
        reporte.titulo = "Listado de Alumnos de Cuotas Pagadas"
        sql = sqlAlumnos(request)
        reporte.posicion = landscape(A4)
        reporte.cantidad ="Cantidad de Cuotas Pagadas: " 
       
        sqlTotal = ""
        sqlTotal += "     select sum(pc_aux.importe) as total "  
        sqlTotal += "     from pago_insc_cuota pc_aux "
        sqlTotal += "     inner join inscripcion i on i.id_inscripcion = pc_aux.id_inscripcion "
        sqlTotal += "     inner join alumno a on a.id_alumno = i.id_alumno "  
        sqlTotal += "     inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
        sqlTotal += "     inner join curso curso on curso.id_curso = periodo.id_curso "
        sqlTotal += "     inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
        sqlTotal += "     WHERE 1=1 "
        
        if request.GET["cbxAnio"]!= '':
            sqlTotal += " and year(pc_aux.fecha_pago) = " + request.GET["cbxAnio"]
        
        if request.GET["cbxMes"]!= '':
            sqlTotal += " and month(pc_aux.fecha_pago) = " + request.GET["cbxMes"]
        
        if request.GET["id_periodo_curso"] != '':
            sqlTotal += " and periodo.id_periodo_curso = " + request.GET["id_periodo_curso"]
            
        if request.GET["id_alumno"] != '':
            sqlTotal += " and a.id_alumno = '" + request.GET["id_alumno"] + "' "        
        print("TOTAL: " + sqlTotal)
        cursor = connection.cursor()
        cursor.execute(sqlTotal)
        rows = cursor.fetchall()
        cursor.close()
            
        for row in rows:
            if(row[0] != None):
                reporte.total = str(float(row[0]))
     
    if reportName == "alumnosMorosos":        
        genericStyle(reporte)
        reporte.titulo = "Listado de Alumnos Morosos"
        sql = sqlAlumnosMorosos(request)
        reporte.posicion = landscape(A4)
        reporte.cantidad ="Cantidad de Inscripciones: "   
    if reportName == "balance":
        genericStyle(reporte)
        reporte.titulo = "Informe de balance"
        sql = sqlBalance(request)        
    if reportName == "totales":
        reporte.titulo = "Informe de Movimientos Totales"
        sql = sqlTotales(request)
    print(sql)
    return sql

def genericStyle(reporte):
    tstyle = [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
              ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
          ('BOX', (0,0), (-1,-1), 0.25, colors.black),]
    tstylepara = tstyle + [('VALIGN',(0,1),(3,-1),'TOP'),]
    reporte.list_style = TableStyle(tstylepara)

def sqlAlumnosImporte(request):
    sql = ""
    sql += " SELECT count(*) as cantidad, sum(cuota.importe) as importe "
    sql += " FROM pago_insc_cuota cuota "
    sql += " inner join inscripcion i on i.id_inscripcion = cuota.id_inscripcion "
    sql += " inner join alumno a on a.id_alumno = i.id_alumno "
    sql += " inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
    sql += " inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += " inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
    sql += " WHERE 1=1 "

    if request.GET["cbxMes"] != '':
        sql += " and month(cuota.fecha_pago) = " + request.GET["cbxMes"]
    if request.GET["cbxAnio"] != '':
        sql += " and year(cuota.fecha_pago) = " + request.GET["cbxAnio"]
    return sql

def sqlAlumnosInscriptos(request):
    sql = " select distinct a.dni as 'Dni', concat(a.apellido, ' ', a.nombre) as 'Apellido y Nombre', concat(curso.nombre, ' - ', idioma.descripcion) as 'Taller' "
    sql += "     FROM alumno a "
    sql += "         inner join inscripcion i on i.id_alumno = a.id_alumno "    
    sql += "         inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
    sql += "         inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += "         inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
    sql += "     WHERE 1=1 "
      
    if request.GET["cbxAnio"] != '':
        sql += " and year(i.fecha_alta) = " + request.GET["cbxAnio"]
        
    if request.GET["cbxAlumno"] != '':
        sql += " and a.id_alumno = " + request.GET["id_alumno"] 

    if request.GET["id_periodo_curso"] != '':
        sql += " and periodo.id_periodo_curso = " + request.GET["id_periodo_curso"]   
        
    sql += " order by a.apellido asc, a.nombre asc"  
    return sql

def sqlAlumnos(request):
    sql = ""
    sql += " SELECT distinct a.dni as 'Dni', concat(a.apellido, ' ', a.nombre) as 'Apellido y Nombre', concat(curso.nombre, ' - ', idioma.descripcion) as 'Taller', "
    sql += " (select group_concat( (case when pc_aux.pagado = true then "    
    
    sql += " case "
    sql += " when month(pc_aux.fecha_cuota) = 1 then 'ENE' "
    sql += " when month(pc_aux.fecha_cuota) = 2 then 'FEB' "
    sql += " when month(pc_aux.fecha_cuota) = 3 then 'MAR' "
    sql += " when month(pc_aux.fecha_cuota) = 4 then 'ABR' "
    sql += " when month(pc_aux.fecha_cuota) = 5 then 'MAY' "
    sql += " when month(pc_aux.fecha_cuota) = 6 then 'JUN' "
    sql += " when month(pc_aux.fecha_cuota) = 7 then 'JUL' "
    sql += " when month(pc_aux.fecha_cuota) = 8 then 'AGO' "
    sql += " when month(pc_aux.fecha_cuota) = 9 then 'SEP' "
    sql += " when month(pc_aux.fecha_cuota) = 10 then 'OCT' "
    sql += " when month(pc_aux.fecha_cuota) = 11 then 'NOV' "
    sql += " when month(pc_aux.fecha_cuota) = 12 then 'DIC' "
    sql += " end "
        
    sql += "  end)  SEPARATOR '|') as meses_cuotas "
    sql += " 	from pago_insc_cuota pc_aux "
    sql += " 	inner join inscripcion i_aux on pc_aux.id_inscripcion = i_aux.id_inscripcion "
    sql += " 	inner join alumno a_aux on a_aux.id_alumno = i_aux.id_alumno "
    sql += "     where i_aux.id_alumno = a.id_alumno and pc_aux.id_inscripcion = i.id_inscripcion and i_aux.id_periodo_curso = periodo.id_periodo_curso "
    if request.GET["cbxAnio"]!= '':
        sql += " and year(pc_aux.fecha_pago) = " + request.GET["cbxAnio"]
    if request.GET["cbxMes"]!= '':
        sql += " and month(pc_aux.fecha_pago) = " + request.GET["cbxMes"]
                
    sql += " 	group by 'all') as 'Cuotas Pagadas', "
    sql += " 	(select sum(pc_aux.importe) as total ";
    sql += " 	    from pago_insc_cuota pc_aux    ";  
    sql += " 	    inner join inscripcion i_aux on pc_aux.id_inscripcion = i_aux.id_inscripcion";      
    sql += " 	    inner join alumno a_aux on a_aux.id_alumno = i_aux.id_alumno    ";  
    sql += " 	    where i_aux.id_alumno = a.id_alumno and pc_aux.id_inscripcion = i.id_inscripcion and i_aux.id_periodo_curso = periodo.id_periodo_curso ";
    if request.GET["cbxAnio"]!= '':
        sql += " and year(pc_aux.fecha_pago) = " + request.GET["cbxAnio"]
    if request.GET["cbxMes"]!= '':
        sql += " and month(pc_aux.fecha_pago) = " + request.GET["cbxMes"]
    
    sql += " 	) as Total ";    
    sql += " 	FROM alumno a "
    sql += " 		inner join inscripcion i on i.id_alumno = a.id_alumno "
    sql += "         inner join pago_insc_cuota pago on pago.id_inscripcion = i.id_inscripcion "
    sql += " 		inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
    sql += " 		inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += " 		inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
    sql += " 	WHERE 1=1 "
    if request.GET["cbxAnio"]!= '':
        sql += " and year(pago.fecha_pago) = " + request.GET["cbxAnio"]
        
    if request.GET["cbxMes"]!= '':
        sql += " and month(pago.fecha_pago) = " + request.GET["cbxMes"]
        
    if request.GET["id_periodo_curso"] != '':
        sql += " and periodo.id_periodo_curso = " + request.GET["id_periodo_curso"]   
        
    sql += " order by a.apellido asc, a.nombre asc"  
    return sql

def sqlAlumnosMorosos(request):
    ''' traer el periodo de la in'''
    
    sql = ""
    sql += " SELECT a.dni as 'Dni', " \
           "concat(a.apellido, ' ', a.nombre) as 'Apellido y Nombre', concat(curso.nombre, ' - ', idioma.descripcion) as 'Taller', "
    sql += " (select group_concat( (case when pc_aux.pagado = true then "    
    
    sql += " case "
    sql += " when month(pc_aux.fecha_cuota) = 1 then 'ENE' "
    sql += " when month(pc_aux.fecha_cuota) = 2 then 'FEB' "
    sql += " when month(pc_aux.fecha_cuota) = 3 then 'MAR' "
    sql += " when month(pc_aux.fecha_cuota) = 4 then 'ABR' "
    sql += " when month(pc_aux.fecha_cuota) = 5 then 'MAY' "
    sql += " when month(pc_aux.fecha_cuota) = 6 then 'JUN' "
    sql += " when month(pc_aux.fecha_cuota) = 7 then 'JUL' "
    sql += " when month(pc_aux.fecha_cuota) = 8 then 'AGO' "
    sql += " when month(pc_aux.fecha_cuota) = 9 then 'SEP' "
    sql += " when month(pc_aux.fecha_cuota) = 10 then 'OCT' "
    sql += " when month(pc_aux.fecha_cuota) = 11 then 'NOV' "
    sql += " when month(pc_aux.fecha_cuota) = 12 then 'DIC' "
    sql += " end "
        
    sql += "  end)  SEPARATOR '|') as meses_cuotas "
    sql += "     from pago_insc_cuota pc_aux "
    sql += "     inner join inscripcion i_aux on pc_aux.id_inscripcion = i_aux.id_inscripcion "
    sql += "     inner join alumno a_aux on a_aux.id_alumno = i_aux.id_alumno "
    sql += "     where i_aux.id_alumno = a.id_alumno and pc_aux.id_inscripcion = i.id_inscripcion and i_aux.id_periodo_curso = periodo.id_periodo_curso "
    sql += "     group by 'all') as 'Cuotas Pagadas' "
    sql += "     FROM alumno a "
    sql += "         inner join inscripcion i on i.id_alumno = a.id_alumno "
    sql += "         inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
    sql += "         inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += "         inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
    sql += "     WHERE 1=1 "

    if request.GET["cbxAnio"] != '':
        sql += " and year(i.fecha_pago) = '" + request.GET["cbxAnio"] + "' "   

    if request.GET["cbxAlumno"] != '':
        sql += " and a.id_alumno = '" + request.GET["id_alumno"] + "' "

    if request.GET["cbxCurso"] != '':
        sql += " and curso.id_curso = " + request.GET["id_curso"]

    if request.GET["cbxIdioma"] != '':
        sql += " and idioma.id_idioma = " + request.GET["id_idioma"]     
     
    sql += " Union "
    sql += "select 'Total', '','','','' "  
    sql += "     from pago_insc_cuota pc_aux "
    sql += "     inner join inscripcion i on i.id_inscripcion = pc_aux.id_inscripcion "
    sql += "     inner join alumno a on a.id_alumno = a.id_alumno "  
    sql += "     inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
    sql += "     inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += "     inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
    sql += "     WHERE 1=1 "

    if request.GET["fechaDesde"]!= '':
        sql += " and i.fecha_pago >= '" + sqlDateFormat(request.GET["fechaDesde"]) + " 00:00:00' "

    if request.GET["fechaHasta"] != '':
        sql += " and i.fecha_pago <= '" + sqlDateFormat(request.GET["fechaHasta"]) + " 23:59:59' "
           
    if request.GET["cbxAlumno"] != '':
        sql += " and a.id_alumno = '" + request.GET["id_alumno"] + "' "

    if request.GET["cbxCurso"] != '':
        sql += " and curso.id_curso = " + request.GET["id_curso"]

    if request.GET["cbxIdioma"] != '':
        sql += " and idioma.id_idioma = " + request.GET["id_idioma"] 
       
    sql += " order by a.apellido asc, a.nombre asc"  
    return sql

def sqlBalance(request):    
    sql = ""
    sql += "select  DATE_FORMAT(c.fecha, '%d/%m/%y') as 'fecha', c.concepto , c.descripcion, "
    sql += " (case when c.estado = 'I' then c.importe else 0 end) as entrada, "
    sql += " (case when c.estado = 'E' then c.importe else 0 end) as salida "
    sql += " from v_caja c "   
    sql += " WHERE 1=1 "
    if request.GET["fechaDesde"]!= '':
        sql += " and c.fecha >= '" + sqlDateFormat(request.GET["fechaDesde"]) + " 00:00:00' "

    if request.GET["fechaHasta"] != '':
        sql += " and c.fecha <= '" + sqlDateFormat(request.GET["fechaHasta"]) + " 23:59:59' "


    if request.GET["id_concepto"] != '':
        sql += " and c.id_concepto = " + request.GET["id_concepto"]


    if request.GET["cbxMovimiento"] != '':
        sql += " and c.estado = '" + request.GET["cbxMovimiento"] + "'"
                
    sql += " Union "
    sql += "select 'Total', '','', "  
    if request.GET["cbxMovimiento"] == '' or request.GET["cbxMovimiento"] == 'I':
        sql += " ( "
        sql += "  select sum(c.importe) "
        sql += "    from v_caja c "
        sql += " WHERE 1=1 "
        if request.GET["fechaDesde"]!= '':
            sql += " and c.fecha >= '" + sqlDateFormat(request.GET["fechaDesde"]) + " 00:00:00' "
        if request.GET["fechaHasta"] != '':
            sql += " and c.fecha <= '" + sqlDateFormat(request.GET["fechaHasta"]) + " 23:59:59' "
        if request.GET["id_concepto"] != '':
            sql += " and c.id_concepto = " + request.GET["id_concepto"]
        if request.GET["cbxMovimiento"] != '':
            sql += " and c.estado = '" + request.GET["cbxMovimiento"] + "'"   
        sql += " ) as entrada, "        
    else:
        sql += " '', "
    if request.GET["cbxMovimiento"] == '' or request.GET["cbxMovimiento"] == 'E':
        sql += " ( "
        sql += "  select sum(c.importe) "
        sql += "    from v_caja c "
        sql += " WHERE 1=1  and c.estado = 'E' "
        if request.GET["fechaDesde"]!= '':
            sql += " and c.fecha >= '" + sqlDateFormat(request.GET["fechaDesde"]) + " 00:00:00' "
        if request.GET["fechaHasta"] != '':
            sql += " and c.fecha <= '" + sqlDateFormat(request.GET["fechaHasta"]) + " 23:59:59' "
        if request.GET["id_concepto"] != '':
            sql += " and c.id_concepto = " + request.GET["id_concepto"]
        if request.GET["cbxMovimiento"] != '':
            sql += " and c.estado = '" + request.GET["cbxMovimiento"] + "'"    
        sql += " ) as salida "
    else:
        sql += " '' "
    
    return sql

def sqlTotales(request):
    sql = ""
    sql += " select "
    sql += " 	CASE "
    sql += "      WHEN month(c.fecha) = 1 THEN 'Enero'  "
    sql += "      WHEN month(c.fecha) = 2 THEN 'Febrero' "
    sql += "      WHEN month(c.fecha) = 3 THEN 'Marzo' "
    sql += "      WHEN month(c.fecha) = 4 THEN 'Abril' "
    sql += "      WHEN month(c.fecha) = 5 THEN 'Mayo' "
    sql += "      WHEN month(c.fecha) = 6 THEN 'Junio' "
    sql += "      WHEN month(c.fecha) = 7 THEN 'Julio' "
    sql += "      WHEN month(c.fecha) = 8 THEN 'Agosto' "
    sql += "      WHEN month(c.fecha) = 9 THEN 'Septiembre' "
    sql += "      WHEN month(c.fecha) = 10 THEN 'Octubre' "
    sql += "      WHEN month(c.fecha) = 11 THEN 'Noviembre' "
    sql += "      WHEN month(c.fecha) = 12 THEN 'Diciembre' "
    sql += "     END  "
    sql += " 	as 'Mes', "
    sql += " 	concep.descripcion as 'Concepto', "
    sql += "     (case when c.estado = 'I' then  sum(c.importe)  end) as 'Entrada($)', "
    sql += " 	(case when c.estado = 'E' then  sum(c.importe)  end) as 'Salida($)' "
    sql += " from caja c "
    sql += " left join concepto concep on concep.id_concepto = c.id_concepto "
    sql += " WHERE 1=1 "

    if request.GET["cbxAnio"] != '':
        sql += " and year(c.fecha) = '" + request.GET["cbxAnio"] + "' "

    sql += " group by month(c.fecha), concep.descripcion, c.estado "
    return sql

def generar_reporte_csv(request):    
    sReportName = request.GET['report_name']
    # Creamos el objeto Httpresponse con la cabecera CSV apropiada.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + sReportName + '.csv'
 
    # Creamos un escritor CSV usando a HttpResponse como "fichero"    
    writer = csv.writer(response, delimiter=';' , dialect='excel')
    
    reporte = ReportCSV()
    sql = getQueryReportCSV(request, sReportName, reporte)    
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()

    writer.writerow([i[0] for i in cursor.description])
    for row in rows:
        writer.writerow([row[0], row[1]])
 
    return response

def getQueryReportCSV(request, reportName, reporteCSV):
    sql = ""
    if reportName == "alumnosInscriptos":
        reporteCSV.titulo = "Lista de Alumnos"
        sql = sqlListaAlumnoCSV(request)    
        print(sql)
    return sql

def sqlListaAlumnoCSV(request):
    sql = ""
    sql += " SELECT distinct a.apellido as 'Apellido', a.nombre as 'Nombre' "
    sql += "     FROM alumno a "
    sql += "         inner join inscripcion i on i.id_alumno = a.id_alumno "
    sql += "         inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso "
    sql += "         inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += "         inner join idioma idioma on idioma.id_idioma = periodo.id_idioma "
    sql += "     WHERE 1=1 "
    
    if request.GET["cbxAnio"] != '':
        sql += " and year(i.fecha_alta) = '" + request.GET["cbxAnio"] + "' "

    if request.GET["cbxAlumno"] != '':
        sql += " and a.id_alumno = '" + request.GET["id_alumno"] + "' "

    if request.GET["id_periodo_curso"] != '':
        sql += " and periodo.id_periodo_curso = " + request.GET["id_periodo_curso"]  
        
    sql += " order by a.apellido asc, a.nombre asc"
    return sql
        

def ticket(request):    
    sReportName = 'Ticket'
    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()         
    
    sql = ""
    sql += " select concat(a.apellido, ' ',a.nombre) as apellido_y_nombre, "
    sql += "     curso.nombre as taller, "
    sql += "     idioma.descripcion as curso, "
    sql += "     concat ((CASE "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 1 THEN 'Enero'  "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 2 THEN 'Febrero' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 3 THEN 'Marzo' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 4 THEN 'Abril' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 5 THEN 'Mayo' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 6 THEN 'Junio' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 7 THEN 'Julio' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 8 THEN 'Agosto' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 9 THEN 'Septiembre' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 10 THEN 'Octubre' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 11 THEN 'Noviembre' "
    sql += "      WHEN month(pc_aux.fecha_cuota) = 12 THEN 'Diciembre' "
    sql += "     END), ' ', year(pc_aux.fecha_cuota)), DATE_FORMAT( CURRENT_TIMESTAMP(), '%d/%m/%Y %H:%i') as fecha, "   
    sql += "      a.dni, "
    sql += "      pc_aux.importe "
    sql += " from pago_insc_cuota pc_aux " 
    sql += " inner join inscripcion i on i.id_inscripcion = pc_aux.id_inscripcion " 
    sql += " inner join alumno a on a.id_alumno = i.id_alumno "
    sql += " inner join periodo_curso periodo on periodo.id_periodo_curso = i.id_periodo_curso " 
    sql += " inner join curso curso on curso.id_curso = periodo.id_curso "
    sql += " inner join idioma idioma on idioma.id_idioma = periodo.id_idioma " 
    sql += " where pc_aux.id_pago_insc_cuota = " + request.GET['id_pago_insc_cuota']
    print(sql)
    
    doc = _page_properties(sReportName, buff, A5,40,40,60,18)  
    builder = []
    styles = getSampleStyleSheet()
    header = Paragraph("Asoc. Flia. Abruzzesa", styles['Heading1'])   
    builder.append(header)
       
    # Data retrieval operation - no commit required
    cursor = connection.cursor()
    cursor.execute(sql)   
    rows = cursor.fetchall()            
    for row in rows:
        header = Paragraph('Fecha: ' + row[4], styles['Heading3'])
        builder.append(header)
        header = Paragraph('Dni: ' + row[5], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Apellido y Nombre: ' + row[0], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Taller: ' + row[1], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Curso: ' + row[2], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Correspondiente a: ' + row[3], styles['Heading3'])   
        builder.append(header)        
        header = Paragraph('Importe: ' + str(row[6]), styles['Heading3']) 
        builder.append(header)  
    cursor.close()
    header = Paragraph('Comprobante Interno', styles['Heading5'])   
    builder.append(header) 
                  
    header = Paragraph("", styles['Heading1'])   
    for x in range(1, 5):
        builder.append(header) 
    
    header = Paragraph("-------------------------------------------------------------------", styles['Heading5'])   
    builder.append(header)  
    header = Paragraph("", styles['Heading1'])   
    for x in range(1, 5):
        builder.append(header)  
              
    header = Paragraph("Asoc. Flia. Abruzzesa", styles['Heading1'])   
    builder.append(header)   
    cursor = connection.cursor()
    cursor.execute(sql)   
    rows = cursor.fetchall()               
    for row in rows:
        header = Paragraph('Fecha: ' + row[4], styles['Heading3'])     
        builder.append(header)
        header = Paragraph('Dni: ' + row[5], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Apellido y Nombre: ' + row[0], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Taller: ' + row[1], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Curso: ' + row[2], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Correspondiente a: ' + row[3], styles['Heading3'])           
        builder.append(header)          
    cursor.close() 
    header = Paragraph('Comprobante Interno', styles['Heading5'])   
    builder.append(header) 
                   
    doc.build(builder)
    response.write(buff.getvalue())
    buff.close()   
    
    return response


def ticket_socio(request):    
    sReportName = 'Ticket Socio'
    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()         
    
    sql = ""
    sql += " select concat(a.apellido, ' ',a.nombre) as apellido_y_nombre, "
    sql += "     concat((CASE "
    sql += "      WHEN pc_aux.nro_cuota = 1 THEN 'Cuota 1'  "
    sql += "      WHEN pc_aux.nro_cuota = 2 THEN 'Cuota 2' "
    sql += "      WHEN pc_aux.nro_cuota = 3 THEN 'Cuota 3' "
    sql += "      WHEN pc_aux.nro_cuota = 4 THEN 'Cuota 4' "
    sql += "     END), ' | ', DATE_FORMAT( CURRENT_TIMESTAMP(), '%d/%m/%Y %H:%i')) as fecha, "   
    sql += "      a.dni, "
    sql += "      pc_aux.importe "
    sql += " from pago_insc_cuota_socio pc_aux " 
    sql += " inner join alumno a on a.id_alumno = pc_aux.id_alumno "
    sql += " where pc_aux.id_pago_insc_cuota_soc = " + request.GET['id_pago_insc_cuota_soc']
    print(sql)
    
    doc = _page_properties(sReportName, buff, A5,40,40,60,18)  
    builder = []
    styles = getSampleStyleSheet()
    header = Paragraph("Asoc. Flia. Abruzzesa", styles['Heading1'])   
    builder.append(header)
       
    # Data retrieval operation - no commit required
    cursor = connection.cursor()
    cursor.execute(sql)   
    rows = cursor.fetchall()            
    for row in rows:
        header = Paragraph('Fecha: ' + str(row[1]), styles['Heading3'])
        builder.append(header)
        header = Paragraph('Dni: ' + row[2], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Apellido y Nombre: ' + row[0], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Correspondiente a: ' + str(row[2]), styles['Heading3'])   
        builder.append(header)        
        header = Paragraph('Importe: ' + str(row[3]), styles['Heading3']) 
        builder.append(header)  
    cursor.close()
    header = Paragraph('Comprobante Interno', styles['Heading5'])   
    builder.append(header) 
                  
    header = Paragraph("", styles['Heading1'])   
    for x in range(1, 5):
        builder.append(header) 
    
    header = Paragraph("-------------------------------------------------------------------", styles['Heading5'])   
    builder.append(header)  
    header = Paragraph("", styles['Heading1'])   
    for x in range(1, 5):
        builder.append(header)  
              
    header = Paragraph("Asoc. Flia. Abruzzesa", styles['Heading1'])   
    builder.append(header)   
    cursor = connection.cursor()
    cursor.execute(sql)   
    rows = cursor.fetchall()               
    for row in rows:
        header = Paragraph('Fecha: ' + str(row[1]), styles['Heading3'])
        builder.append(header)
        header = Paragraph('Dni: ' + row[2], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Apellido y Nombre: ' + row[0], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Correspondiente a: ' + str(row[2]), styles['Heading3'])   
        builder.append(header)        
        header = Paragraph('Importe: ' + str(row[3]), styles['Heading3']) 
        builder.append(header)            
    cursor.close() 
    header = Paragraph('Comprobante Interno', styles['Heading5'])   
    builder.append(header) 
                   
    doc.build(builder)
    response.write(buff.getvalue())
    buff.close()   
    
    return response

def comprobante_caja(request):    
    sReportName = 'Comprobante Caja'
    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()         
    
    sql = ""
    sql += " select DATE_FORMAT( c.fecha, '%d/%m/%Y %H:%i') as fecha, c.descripcion, co.descripcion as concepto, c.importe "
    sql += " from caja c "
    sql += " inner join concepto co on co.id_concepto = c.id_concepto "
    sql += " where c.id_caja = " + request.GET['id_caja']
    print(sql)
    
    doc = _page_properties(sReportName, buff, A5,40,40,60,18)  
    builder = []
    styles = getSampleStyleSheet()
    header = Paragraph("Asoc. Flia. Abruzzesa", styles['Heading1'])   
    builder.append(header)
       
    # Data retrieval operation - no commit required
    cursor = connection.cursor()
    cursor.execute(sql)   
    rows = cursor.fetchall()            
    for row in rows:
        header = Paragraph('Fecha: ' + str(row[0]), styles['Heading3'])
        builder.append(header)
        header = Paragraph('Concepto: ' + row[2], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Descripción: ' + row[1], styles['Heading3'])   
        builder.append(header)              
        header = Paragraph('Importe: ' + str(row[3]), styles['Heading3']) 
        builder.append(header)  
    cursor.close()
    header = Paragraph('Comprobante Interno', styles['Heading5'])   
    builder.append(header) 
                  
    header = Paragraph("", styles['Heading1'])   
    for x in range(1, 5):
        builder.append(header) 
    
    header = Paragraph("-------------------------------------------------------------------", styles['Heading5'])   
    builder.append(header)  
    header = Paragraph("", styles['Heading1'])   
    for x in range(1, 5):
        builder.append(header)  
              
    header = Paragraph("Asoc. Flia. Abruzzesa", styles['Heading1'])   
    builder.append(header)   
    cursor = connection.cursor()
    cursor.execute(sql)   
    rows = cursor.fetchall()               
    for row in rows:
        header = Paragraph('Fecha: ' + str(row[0]), styles['Heading3'])
        builder.append(header)
        header = Paragraph('Concepto: ' + row[2], styles['Heading3'])   
        builder.append(header)
        header = Paragraph('Descripción: ' + row[1], styles['Heading3'])   
        builder.append(header)              
        header = Paragraph('Importe: ' + str(row[3]), styles['Heading3']) 
        builder.append(header)              
    cursor.close() 
    header = Paragraph('Comprobante Interno', styles['Heading5'])   
    builder.append(header) 
                   
    doc.build(builder)
    response.write(buff.getvalue())
    buff.close()   
    
    return response
