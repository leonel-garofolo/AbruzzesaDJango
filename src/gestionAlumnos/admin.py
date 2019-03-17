from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectAdminStackedInline
from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from . import reports
from .forms import AlumnoForm
from .models import Concepto, Configuracion, Curso, Idioma, Alumno, Inscripcion, PeriodoCurso, Caja, PagoInscCuota, PagoInscCuotaSocio, ModificarInscripcionSocio, ModificarInscripcion

class ConceptoAdmin(admin.ModelAdmin):   
    search_fields = ('descripcion', 'descripcion')
admin.site.register(Concepto, ConceptoAdmin)

class ConfiguracionAdmin(admin.ModelAdmin):   
    form = make_ajax_form(Configuracion, {'id_concepto_pago_asoc': 'id_concepto',
                                          'id_concepto_pago_insc': 'id_concepto',})    
admin.site.register(Configuracion, ConfiguracionAdmin)


class InscripcionInline(AjaxSelectAdminStackedInline):
    # Example of the stacked inline
    model = Inscripcion
    form = make_ajax_form(Inscripcion, {
        'id_periodo_curso': 'id_periodo_curso',            
    })
    extra = 1
    
class AlumnoAdmin(AjaxSelectAdmin):  
    list_display = ('dni', 'apellido', 'nombre', 'fecha_nacimiento', 'telefono', 'celular', 'correo')
    search_fields = ('dni', 'apellido', 'nombre', 'telefono', 'celular')   
    inlines = [
        InscripcionInline
    ] 
        
admin.site.register(Alumno, AlumnoAdmin)

class PeriodoCursoAdmin(AjaxSelectAdmin):
    list_display = ('id_curso', 'id_idioma', 'fecha_inicio', 'fecha_fin', 'importe_inscripcion', 'importe')
    search_fields = ('id_curso__nombre', 'id_idioma__descripcion')
    form = make_ajax_form(PeriodoCurso, {'id_curso': 'id_curso', 'id_idioma': 'id_idioma'})
admin.site.register(PeriodoCurso, PeriodoCursoAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
admin.site.register(Curso, CursoAdmin)

class IdiomaAdmin(admin.ModelAdmin):
    search_fields = ('id_idioma','descripcion')
admin.site.register(Idioma,IdiomaAdmin)

class InscripcionAdmin(AjaxSelectAdmin):
    list_display = ('fecha_alta', 'id_alumno', 'id_periodo_curso', 'estado')
    search_fields = ('fecha_alta', 'id_alumno__nombre', 'id_periodo_curso__id_curso__nombre')
    form = make_ajax_form(Inscripcion, {
        'id_alumno': 'id_alumno',
        'id_periodo_curso': 'id_periodo_curso'
        })
admin.site.register(Inscripcion, InscripcionAdmin)

class CajaAdmin(AjaxSelectAdmin):
    change_form_template = "admin/caja/caja_form.html"
    readonly_fields = ('id_caja',)
    list_display = ('id_concepto', 'descripcion', 'importe', 'estado')
    search_fields = ('id_concepto__descripcion', 'descripcion')
    form = make_ajax_form(Caja, {'id_concepto': 'id_concepto'})
    def has_delete_permission(self, request, obj=None):
        return False
    def get_actions(self, request):
        actions = super(CajaAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions   
admin.site.register(Caja, CajaAdmin)

class PagoInscCuotaAdmin(AjaxSelectAdmin):
    list_display = ('fecha_alta', 'id_inscripcion', 'importe')
    search_fields = ('id_pago_insc_cuota', 'id_inscripcion__id_alumno__apellido')
    form = make_ajax_form(PagoInscCuota, {
        'id_inscripcion': 'id_inscripcion',
        'id_caja': 'id_caja'
    })
admin.site.register(PagoInscCuota, PagoInscCuotaAdmin)

class PagoInscCuotaSocioAdmin(AjaxSelectAdmin):
    list_display = ('fecha_alta', 'importe')
    search_fields = ('id_pago_insc_cuota_soc', 'id_alumno')
    form = make_ajax_form(PagoInscCuotaSocio, {
        'id_caja': 'id_caja'
    })
admin.site.register(PagoInscCuotaSocio, PagoInscCuotaSocioAdmin)


class ModificarInscripcionAdmin(admin.ModelAdmin):  
    pass        
admin.site.register(ModificarInscripcion, ModificarInscripcionAdmin)

class ModificarInscripcionSocioAdmin(admin.ModelAdmin):  
    pass        
admin.site.register(ModificarInscripcionSocio, ModificarInscripcionSocioAdmin)

