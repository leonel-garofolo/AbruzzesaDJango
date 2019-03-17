import json, datetime

from django.db import connection
from django.db.models import Q
from django.http import HttpResponse

from .models import Curso, Idioma, Alumno, Concepto, Inscripcion, PeriodoCurso


def e_alumno(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Alumno.objects.filter(Q(dni__icontains = q)
                                      | Q(nombre__icontains = q)
                                      | Q(apellido__icontains = q))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_alumno
            drug_json['label'] = drug.dni + ' - ' + drug.nombre + ' ' + drug.apellido
            drug_json['value'] = drug.dni + ' - ' + drug.nombre + ' ' + drug.apellido
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_curso(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Curso.objects.filter(Q(descripcion__icontains = q) | Q(nombre__icontains=q))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_curso
            drug_json['label'] = drug.nombre
            drug_json['value'] = drug.nombre
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_idioma(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Idioma.objects.filter(Q(descripcion__icontains = q))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_idioma
            drug_json['label'] = drug.descripcion
            drug_json['value'] = drug.descripcion
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_periodo(request):
    if request.is_ajax():
        q = request.GET.get('q', '')
        year = request.GET["year"]
        
        sql = ""
        sql += " select p.id_periodo_curso, concat(c.nombre, ' - ', i.descripcion) as detalle "
        sql += " from periodo_curso p "
        sql += " inner join idioma i on i.id_idioma = p.id_idioma "
        sql += " inner join curso c on c.id_curso = p.id_curso "
        sql += " where year(p.fecha_alta) = " + year + " and (c.nombre like '%" + q + "%' or i.descripcion like '%" + q + "%')"       
        print(sql)
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        
        results = []    
        for row in rows:
            drug_json = {}
            drug_json['id'] =  row[0]
            drug_json['label'] = row[1]
            drug_json['value'] = row[1]
            results.append(drug_json)
                           
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_periodo_anterior(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        year = datetime.date.today().year
        drugs = PeriodoCurso.objects.filter(Q(fecha_alta__icontains=year) & (Q(id_idioma__descripcion__icontains = q) | Q(id_curso__nombre__icontains = q)))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_periodo_curso
            drug_json['label'] = drug.id_curso.nombre + ' - ' + drug.id_idioma.descripcion
            drug_json['value'] = drug.id_curso.nombre + ' - ' + drug.id_idioma.descripcion
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_periodo_posterior(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        year = datetime.date.today().year
        drugs = PeriodoCurso.objects.filter(Q(fecha_alta__icontains=year) & (Q(id_idioma__descripcion__icontains = q) | Q(id_curso__nombre__icontains = q)))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_periodo_curso
            drug_json['label'] = drug.id_curso.nombre + ' - ' + drug.id_idioma.descripcion
            drug_json['value'] = drug.id_curso.nombre + ' - ' + drug.id_idioma.descripcion
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_concepto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Concepto.objects.filter(Q(descripcion__icontains = q))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_concepto
            drug_json['label'] = drug.descripcion
            drug_json['value'] = drug.descripcion
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def e_inscripcion(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        year = datetime.date.today().year
        drugs = Inscripcion.objects.filter(Q(fecha_alta__icontains=year) & (Q(id_alumno__dni__icontains = q)
                                           | Q(id_alumno__nombre__icontains = q)
                                           | Q(id_alumno__apellido__icontains = q)
                                           | Q(id_periodo_curso__id_curso__nombre__icontains = q)
                                           | Q(id_periodo_curso__id_idioma__descripcion__icontains = q)))[:7]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id_inscripcion
            drug_json['label'] = drug.id_alumno.dni + ' - ' + drug.id_alumno.nombre + ' ' + drug.id_alumno.apellido + ' - ' + drug.id_periodo_curso.id_curso.nombre + ' ' + drug.id_periodo_curso.id_idioma.descripcion
            drug_json['value'] = drug.id_alumno.dni + ' - ' + drug.id_alumno.nombre + ' ' + drug.id_alumno.apellido + ' - ' + drug.id_periodo_curso.id_curso.nombre + ' ' + drug.id_periodo_curso.id_idioma.descripcion 
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = "fail"

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
