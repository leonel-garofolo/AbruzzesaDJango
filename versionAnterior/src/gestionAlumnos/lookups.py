from __future__ import unicode_literals
import datetime
from django.utils.six import text_type
from django.db.models import Q
from django.utils.html import escape
from .models import Alumno, Idioma, PeriodoCurso, Curso, Concepto, Inscripcion, Caja
import ajax_select
from ajax_select import register, LookupChannel


@ajax_select.register('id_alumno')
class AlumnoLookup(LookupChannel):

    model = Alumno

    def get_query(self, q, request):
        return Alumno.objects.filter(Q(dni__icontains=q) | Q(nombre__icontains=q) | Q(apellido__icontains=q)).order_by('apellido', 'nombre')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.nombre

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.dni), escape(obj.apellido) + ' ' +  escape(obj.nombre))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "%s<div><i>%s</i></div>" % (escape(obj.dni), escape(obj.apellido) + ' ' +  escape(obj.nombre))
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True

@ajax_select.register('id_curso')
class CursoLookup(LookupChannel):
    model = Curso

    def get_query(self, q, request):
        return Curso.objects.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q)).order_by('nombre')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.nombre

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "<div><i>%s</i></div>" % (escape(obj.nombre))
        # return self.format_item_display(obj)
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True
    
@ajax_select.register('id_idioma')
class IdiomaLookup(LookupChannel):
    model = Idioma

    def get_query(self, q, request):
        return Idioma.objects.filter(Q(descripcion__icontains=q)).order_by('descripcion')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.descripcion

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "<div><i>%s</i></div>" % (escape(obj.descripcion))
        # return self.format_item_display(obj)
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True

@ajax_select.register('id_periodo_curso')
class PeriodoCursoLookup(LookupChannel):
    model = PeriodoCurso

    def get_query(self, q, request):
        year = datetime.date.today().year
        return PeriodoCurso.objects.filter(Q(fecha_alta__icontains=year) & Q(id_curso__nombre__icontains=q)).order_by('id_curso__nombre')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.id_curso.nombre

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.id_curso.nombre), escape(obj.id_idioma.descripcion))
        # return self.format_item_display(obj)
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True

@ajax_select.register('id_concepto')
class ConceptoLookup(LookupChannel):
    model = Concepto

    def get_query(self, q, request):
        return Concepto.objects.filter(Q(descripcion__icontains=q)).order_by('descripcion')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.descripcion

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "<div><i>%s</i></div>" % (escape(obj.descripcion))
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True

@ajax_select.register('id_inscripcion')
class InscripcionLookup(LookupChannel):
    model = Inscripcion

    def get_query(self, q, request):
        return Inscripcion.objects.filter(
            Q(id_alumno__dni__icontains=q)
            | Q(id_alumno__nombre__icontains=q)
            | Q(id_alumno__apellido__icontains=q)).order_by('id_alumno__apellido', 'id_alumno__nombre')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.id_alumno.apellido

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.id_alumno.apellido), escape(obj.id_alumno.nombre))
        # return self.format_item_display(obj)
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True

@ajax_select.register('id_caja')
class CajaLookup(LookupChannel):
    model = Caja

    def get_query(self, q, request):
        return Caja.objects.filter(
            Q(id_concepto__descripcion__icontains=q)
            | Q(descripcion__icontains=q)).order_by('id_concepto__descripcion', 'descripcion')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.id_concepto.descripcion

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s<div><i>%s</i></div>" % (escape(obj.id_concepto.descripcion), escape(obj.descripcion))
        # return self.format_item_display(obj)
    def can_add(self, user, model):
        """ customize can_add by allowing anybody to add a Group.
            the superclass implementation uses django's permissions system to check.
            only those allowed to add will be offered a [+ add] popup link
            """
        return True