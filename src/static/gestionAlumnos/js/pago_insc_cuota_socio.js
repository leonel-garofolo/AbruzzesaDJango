$(document).ready(function() {
	$("#btnTicket").click(function(){
		printTicket();
	});
	
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
});

function getCuotas() {
	var options = [];
	$("#cbxCuota").html(options);
	$.ajax({
		type : "POST",
		url : '/admin/function/get_tri_cuotas_socio',
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
	        });
		}
	});
	
	$.ajax({
		type : "POST",
		url : '/admin/function/get_importe_inscripcion',
		data : {
			id_alumno : $("#id_inscripcion").val()
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

function save(){	
	if($('#txtImporte').val() == ''){
		alert('Debe ingresar un importe para guardar el pago.');
		return;
	}
	
	$.ajax({
		type : "POST",
		url : '/admin/function/save_insc_cuota_socio',
		data : {
			id_alumno : $("#id_inscripcion").val(),
			nro_cuota : $("#cbxCuota").val(),
			importe: $("#txtImporte").val()
		},
		success : function(response) {			
			$('#id_pago_insc_cuota').val(response);
			printTicket();
			alert('Se realizo el pago.');			
			limpiar('frmCuota');
			$("#cbxInscripcion").focus();
		}
	});	
}

function printTicket(){	
	$('#pdf-iframe').attr("src", '/admin/function/ticketsocio?id_pago_insc_cuota_soc=' + $('#id_pago_insc_cuota').val()).load(function(){
	    document.getElementById('pdf-iframe').contentWindow.print();
	});
	
}