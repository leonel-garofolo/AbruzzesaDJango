$(document).ready(function() {	
	$("#cbxInscripcion").autocomplete({
		source : '/admin/explorer/e_inscripcion_socios',
		minLength : 1,
		change : function(ev, ui) {
			if (!ui.item) {
				$(this).val('');
			}
		},
		select : function(event, ui) {
			var origEvent = event;
			if (origEvent.type == 'autocompleteselect') {
				$("#cbxInscripcion").val(ui.item.value);
			}
			while (origEvent.originalEvent !== undefined)
				origEvent = origEvent.originalEvent;
			if (origEvent.type == 'keydown')
				$("#cbxInscripcion").click();
			$("#id_inscripcion").val(ui.item.id);
			getCuotas();			
		}
	});
	
	$( "#cbxCuota" ).change(function() {
		getImporte();
	});
	$("#cbxInscripcion").focus();
	
	$( "#btnUpdate" ).click(function() {		
		update();
	});
	$( "#btnDelete" ).click(function() {
		deleteCuota();
	});
	$( "#btnImprimir" ).click(function() {
		imprimir();
	});
});

function getCuotas() {
	var options = [];
	$("#cbxCuota").html(options);
	$.ajax({
		type : "POST",
		url : '/admin/function/get_cuotas_socios_pagas',
		data : {
			id_alumno : $("#id_inscripcion").val()
		},
		success : function(json) {	
			console.log(json)
			$.each(json, function(i, value) {				
				var options = '';
				for (var i = 0; i < value.length; i++) {				
					options += '<option value="' + value[i][0] + '">'
							+ value[i][1] + '</option>';					
				}
				$("select#cbxCuota").html(options);
				getImporte();
	        });
		}
	});		
}

function getImporte(){
	var idCuota = $("#cbxCuota").val();
	if(idCuota != null){
		$.ajax({
			type : "POST",
			url : '/admin/function/get_importe_socio_pagado',
			data : {
				nro_cuota : $("#cbxCuota").val()
			},
			success : function(json) {
				$.each(json, function(i, value) {				
					var options = '';
					for (var i = 0; i < value.length; i++) {				
						$("#txtImporte").val(value[i]);
						break;
					}				
		        });			
			}
		});
	}
}

function update(){	
	if($('#txtImporte').val() == ''){
		alert('Debe ingresar un importe para guardar el pago.');
		return;
	}
	
	$.ajax({
		type : "POST",
		url : '/admin/function/update_socio_cuota',
		data : {		
			nro_cuota : $("#cbxCuota").val(),
			importe: $("#txtImporte").val()
		},
		success : function(response) {	
			alert('Se realizo la modificacion.');			
			limpiar('frmCuota');
			$("#cbxInscripcion").focus();
		}
	});	
}

function deleteCuota(){		
	$.ajax({
		type : "POST",
		url : '/admin/function/delete_socio_cuota',
		data : {
			nro_cuota : $("#cbxCuota").val()
		},
		success : function(response) {	
			alert('Se elimino el pago.');			
			limpiar('frmCuota');
			$("#cbxInscripcion").focus();
		}
	});	
}

function imprimir(){	
	if($('#txtImporte').val() == ''){
		alert('Debe ingresar un importe para guardar el pago.');
		return;
	}
	
	printTicket();
}

function printTicket(){	
	$('#pdf-iframe').attr("src", '/admin/function/ticketsocio?id_pago_insc_cuota_soc=' + $('#cbxCuota').val()).load(function(){
	    document.getElementById('pdf-iframe').contentWindow.print();
	});	
}