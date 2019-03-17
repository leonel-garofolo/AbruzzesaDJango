var tblDesde= null;
var tblHasta= null;

$(document).ready(function() {	
	explorer("id_periodo_origen","cbxPeriodoOrigen","e_periodo_anterior");	
	explorer("id_periodo_destino","cbxPeriodoDestino","e_periodo_posterior");
	
	$('#btnCargar').click( function () { cargar();} );	
	$('#btnLimpiar').click( function () { limpiar();} );
	$('#btnInscribirLista').click( function () { inscribirLista();} );
		
	tblDesde= datatable("tblDesde");
	tblHasta= datatable("tblHasta");
	
	$('#btnEnviarTodos').click( function () {		
		tblHasta.rows.add(tblDesde.rows().data()).draw();
		tblDesde.clear().draw();  	
    } );
	
	$('#btnBorrarTodos').click( function () {
		tblDesde.rows.add(tblHasta.rows().data()).draw();
		tblHasta.clear().draw();     
    } );
	
	$('#btnEnviarSeleccionado').click( function () {
		$.each(tblDesde.rows( '.selected' ).indexes(), function( index, value ) {			  
				tblHasta.row.add(tblDesde.row(value).data()).draw();
				tblDesde.row(value).remove().draw();			
			});
        
    } );
	
	$('#btnBorrarSeleccionado').click( function () {
		$.each(tblHasta.rows( '.selected' ).indexes(), function( index, value ) {			  
				tblDesde.row.add(tblHasta.row(value).data()).draw();
				tblHasta.row(value).remove().draw();			
			});
        
    } );
	$("#cbxPeriodoOrigen").focus();
});

function limpiar() {
	$(':input', '#frmCuota').not(':button, :submit, :reset, :hidden').val('')
			.removeAttr('checked').removeAttr('selected');
	tblDesde.clear().draw(); 
	tblHasta.clear().draw(); 
}

function cargar(){
	if($('#id_periodo_origen').val() == ''){
		alert('El Taller de origen es obligatorio.');
		return;
	}	
	if($('#id_periodo_destino').val() == ''){
		alert('El Taller de destino es obligatorio.');
		return;
	}
	
	if($('#id_periodo_origen').val() == $('#id_periodo_destino').val()){
		alert('El Taller de origen debe ser distinto al destino.');
		return;
	}
	
	var data = {		
		"id_periodo_origen": $('#id_periodo_origen').val(),	
		"id_periodo_destino": $('#id_periodo_destino').val()
	};
	$.ajax({
		type : "POST",
		url : '/admin/gestionAlumnos/inscripcion/cargar',
		data : data,
		success : function(json) {				
			if(json.alumnosDesde.length > 0){
				tblDesde.clear().rows.add(json.alumnosDesde).draw();	
			}else{
				alert("Los alumnos del taller de origen ya fueron cargados en el taller de destino.");
			}						
		}
	});
}

function inscribirLista(){
	if ( ! tblHasta.data().count() ) {
	    alert( "Es necesario inscribir al menos un alumno en el taller de destino.");
	}else{	
		var i=0;
		var alumnos=new Array(1); 
		tblHasta.column(0).data().each( function ( value, index ) {
	    	alumnos[i]=value;	       
	        i++;
	    } ); 						
		
		$.ajax({
			type : "POST",					
			url : '/admin/gestionAlumnos/inscripcion/save',
			data : {
				"id_periodo_destino": $('#id_periodo_destino').val(),
				"alumnos[]": alumnos
			},
			success : function(json) {				
				alert('Las inscripciones se realizaron correctamente.');
				limpiar();				
			}
		});				
	}	
}

