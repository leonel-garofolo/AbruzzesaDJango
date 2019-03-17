# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime
from django.db import models
from django.contrib.auth.models import User
from .get_username import get_username
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from .utils import add_months
from django import forms
from django.contrib import messages
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=45)
    apellido = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)   
    fecha_alta = models.DateTimeField(blank=True, null=True, auto_now=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=90)
    celular = models.CharField(max_length=90, blank=True, null=True)
    correo = models.CharField(max_length=255, blank=True, null=True)
    es_socio = models.BooleanField()
    profesion = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.CharField(max_length=90, blank=True, null=True, editable=False)     
    def save(self, *args, **kwargs):
        self.usuario = str(get_username())
        super(Alumno, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):        
        sql = ""
        sql += " select count(a.id_alumno) as tiene_pago "
        sql += " from pago_insc_cuota pago "
        sql += " inner join inscripcion i on i.id_inscripcion = pago.id_inscripcion "
        sql += " inner join alumno a on a.id_alumno = i.id_alumno "
        sql += " where pago.pagado = 1 and a.id_alumno = " + str(self.id_alumno)        
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        
        bEstado = False
        for row in rows:
            if row[0] >= 1:
                bEstado = True
        
        if bEstado:
            return False
        else:                        
            cursor = connection.cursor()
            cursor.execute("select id_inscripcion from inscripcion where id_alumno = " + str(self.id_alumno))  
            rows = cursor.fetchall()                     
            cursor.close()
            
            for row in rows:
                cursor = connection.cursor()
                cursor.execute("delete from pago_insc_cuota where id_inscripcion = " + str(row[0]))    
                cursor.execute("delete from inscripcion where id_inscripcion = " + str(row[0]))                             
                cursor.close()
                
            super(Alumno, self).delete(*args, **kwargs)           
            
       
    def __str__(self):
        return self.dni + ' - ' + self.apellido + ' - ' + self.nombre 
    class Meta:
        managed = False
        db_table = 'alumno'
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'B - Inscripcion'

class Concepto(models.Model):
    id_concepto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    usuario = models.CharField(max_length=90, blank=True, null=True, editable=False) 
    def save(self, *args, **kwargs):
        self.usuario = str(get_username())
        super(Concepto, self).save(*args, **kwargs)
      
    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'concepto'
        verbose_name_plural = 'G - Concepto'

MOVIMIENTO_CHOICES = (
    ('I', 'Ingreso'),
    ('E', 'Egreso'),
)
class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto', blank=True, null=False, verbose_name='Concepto')
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now=True)
    importe = models.DecimalField(max_digits=19, decimal_places=2)
    estado = models.CharField(max_length=45, blank=False, null=False, choices=MOVIMIENTO_CHOICES)
    usuario = models.CharField(max_length=90, blank=True, null=True, editable=False)
    def save(self, *args, **kwargs):
        self.usuario = str(get_username())
        super(Caja, self).save(*args, **kwargs)
    def __str__(self):
        concepto = ""
        if self.id_concepto is not None:
            concepto = self.id_concepto.descripcion
        return concepto + ' - ' + self.descripcion + '-' + str(self.importe) + ' - ' + self.estado

    class Meta:
        managed = False
        db_table = 'caja'
        verbose_name_plural = 'F - Caja'

class Configuracion(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    id_concepto_pago_asoc = models.CharField(max_length=255, blank=True, null=True)
    id_concepto_pago_insc = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):        
        return self.id_concepto_pago_asoc + '-' + self.id_concepto_pago_insc
    class Meta:
        managed = False
        db_table = 'configuracion'
        verbose_name_plural = 'H - Configuracion'


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.CharField(max_length=90, blank=True, null=True, editable=False) 
    def save(self, *args, **kwargs):
        self.usuario = str(get_username())
        super(Curso, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre 
    class Meta:
        managed = False
        db_table = 'curso'
        verbose_name = 'Carga de Talleres'
        verbose_name_plural = 'D - Carga de Talleres'


class ExamenCurso(models.Model):
    id_examen_curso = models.AutoField(primary_key=True)
    fecha_examen = models.DateTimeField()
    nota = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    id_inscripcion = models.ForeignKey('Inscripcion', models.DO_NOTHING, db_column='id_inscripcion', blank=True, null=True)
    usuario = models.CharField(max_length=90, blank=True, null=True, editable=False) 
    def save(self, *args, **kwargs):
        self.usuario = str(get_username())
        super(ExamenCurso, self).save(*args, **kwargs)
    def __str__(self):
        return self.fecha_examen 
    class Meta:
        managed = False
        db_table = 'examen_curso'


class Idioma(models.Model):
    id_idioma = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    def __str__(self):
        return self.descripcion 
    class Meta:
        managed = False
        db_table = 'idioma'
        verbose_name = 'Carga de Cursos'
        verbose_name_plural = 'E - Carga de Cursos'

ESTADO_CHOICES = (
    ('Inscripto', 'Inscripto'),
    ('Regular', 'Regular'),
    ('Libre', 'Libre'),
)
class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno',verbose_name='Alumno')
    id_periodo_curso = models.ForeignKey('PeriodoCurso', models.DO_NOTHING, db_column='id_periodo_curso', blank=False,
                                         null=False, verbose_name='Semestre Curso')
    estado = models.CharField(max_length=45, blank=False, null=False, choices=ESTADO_CHOICES, default='Inscripto')
    fecha_alta = models.DateTimeField(blank=True, null=True, auto_now=True)
    fecha_pago_insc = models.DateTimeField(blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        bDelete = deleteInscCuotasPagas(self.id_inscripcion)
        if(bDelete == True):
            super(Inscripcion, self).delete(*args, **kwargs)
        else:
            print("No se puede eliminar la inscripcion por cuota paga")
            return "No se puede eliminar la inscripcion por cuota paga"

    def __str__(self):
        return self.id_alumno.nombre + ' ' + self.id_alumno.apellido + ' - ' + self.id_periodo_curso.id_curso.nombre + ' - ' + self.id_periodo_curso.id_idioma.descripcion

    class Meta:
        managed = False
        db_table = 'inscripcion'      
        verbose_name_plural = 'I - Inscripcion Masiva de Alumnos'
        
class ModificarInscripcion(models.Model):
    pass

    class Meta:
        managed = False            
        verbose_name_plural = 'J - Modificar Cuotas Pagadas' 
        
@receiver(post_save, sender=Inscripcion)
def model_post_save(sender, instance, created, *args, **kwargs):
    if not created:
        sql = "select id_alumno, id_periodo_curso from inscripcion where id_inscripcion = " + str(instance.pk) 
        print("no creado: " + sql)
        cursor = connection.cursor()
        cursor.execute(sql)  
        rows = cursor.fetchall()                     
        cursor.close()
        id_alumno_ori = None
        id_periodo_curso_ori = None
        for row in rows:
            id_alumno_ori = row[0]
            id_periodo_curso_ori = row[1]
        #Si cambio una inscripcion compruebo si cambio el alumno y el periodo del curso           
        bChange = False
        if id_alumno_ori != None and instance.id_alumno !=id_alumno_ori:
            bChange = True
        if id_periodo_curso_ori != None and instance.id_periodo_curso != id_periodo_curso_ori:
            bChange = True
        
        #Si cambio valido si puedo borrar las cuotas ingresadas
        if bChange == True:                   
            deleteInscCuotasPagas(instance.pk)
        else:
            print("mensaje que no puede cambiar la inscricipn ya q tiene cuotas pagas")
            return "mensaje que no puede cambiar la inscricipn ya q tiene cuotas pagas"
                
def deleteInscCuotasPagas(id_institucion):
    sql = ""
    sql += " select p.pagado " 
    sql += " from pago_insc_cuota p "
    sql += " inner join inscripcion i on i.id_inscripcion = p.id_inscripcion "
    sql += " inner join periodo_curso pc on pc.id_periodo_curso = i.id_periodo_curso "
    sql += " where i.id_inscripcion = " + str(id_institucion)
    cursor = connection.cursor()
    print("delete: " + sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    bPagado = False
    for row in rows:
        if row[0] == 1:
            bPagado = True
    #delete cuentas cargadas pendientes
    if bPagado == False:                
        cursor = connection.cursor()
        cursor.execute("delete from pago_insc_cuota where id_inscripcion = " + str(id_institucion))                
        cursor.close()
        return True
    else:
        return False   

class PagoInscCuota(models.Model):
    id_pago_insc_cuota = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey(Inscripcion, models.DO_NOTHING, db_column='id_inscripcion')
    fecha_alta = models.DateTimeField(auto_now=True)
    fecha_cuota = models.DateField()
    importe = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    es_socio = models.BooleanField()
    pagado = models.IntegerField(blank=True, null=True)
    id_caja = models.ForeignKey(Caja, models.DO_NOTHING, db_column='id_caja', blank=True, null=True)
    fecha_pago = models.DateTimeField(blank=True, null=True, auto_now=True)
    usuario = models.CharField(max_length=90, blank=True, null=True, editable=False) 
    def save(self, *args, **kwargs):       
        self.usuario = str(get_username())
        super(PagoInscCuota, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Abono de Cuota'
        verbose_name_plural = 'A - Abono de Cuota'
        managed = False
        db_table = 'pago_insc_cuota'
        unique_together = (('id_pago_insc_cuota', 'fecha_alta', 'id_inscripcion'))

class PeriodoCurso(models.Model):
    id_periodo_curso = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_curso', blank=True, null=True, verbose_name='Taller')
    id_idioma = models.ForeignKey(Idioma, models.DO_NOTHING, db_column='id_idioma', blank=True, null=True, verbose_name='Curso')
    fecha_alta = models.DateTimeField(auto_now=True)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    cant_meses = models.IntegerField(editable=False)
    importe = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    importe_inscripcion = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    def save(self, *args, **kwargs):
        months = (self.fecha_fin.year - self.fecha_inicio.year) * 12 + self.fecha_fin.month - self.fecha_inicio.month

        days = (self.fecha_fin - self.fecha_inicio).days
        if days > 16:
            months += 1        
        self.cant_meses= months       
        super(PeriodoCurso, self).save(*args, **kwargs)               
    def delete(self, *args, **kwargs):       
        sql = ""
        sql += " select count(i.id_inscripcion) as tiene_insc "
        sql += " from inscripcion i "
        sql += " inner join periodo_curso pe on pe.id_periodo_curso= i.id_periodo_curso "
        sql += " where pe.id_periodo_curso = " + str(self.id_periodo_curso)        
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        
        bEstado = False
        for row in rows:
            if row[0] >= 1:
                bEstado = True
        
        if bEstado:
            return False
        else:                                    
            super(Alumno, self).delete(*args, **kwargs)
                        
    def __str__(self):
        return  self.id_curso.nombre + ' ' + self.id_idioma.descripcion
    
    class Meta:
        managed = False
        db_table = 'periodo_curso'
        verbose_name = 'Talleres'
        verbose_name_plural = 'C - Talleres'
    
