$(document).ready(function() {
	 var min = 2017;
     max = min + 20;
     select = document.getElementById('cbxAnio');

	 for (var i = min; i<=max; i++){
	     var opt = document.createElement('option');
	     opt.value = i;
	     opt.innerHTML = i;
	     select.appendChild(opt);
	 }
	 select.value = new Date().getFullYear();
	 $('#cbxAnio').change(function(){		 
		 $("#cbxAlumno").val('');
		 $("#id_alumno").val('');
		 
		 $("#cbxPeriodo").val('');
		 $("#id_periodo_curso").val('');
	 });

	$("#cbxPeriodo").autocomplete({
		source : function( request, response ) {
	        $.ajax({
	          url: "/admin/explorer/e_periodo",
	          dataType: "json",
	          data: {
	            year: $("#cbxAnio").val(),
	            q: request.term
	          },
	          success: function( data ) {
	            response( data );
	          }
	        });
	      },
		minLength : 1,
		change : function(ev, ui) {
			if (!ui.item) {
				$(this).val('');
			}
		},
		select : function(event, ui) {
			var origEvent = event;
			if (origEvent.type == 'autocompleteselect') {
				$("#cbxPeriodo").val(ui.item.value);
			}
			while (origEvent.originalEvent !== undefined)
				origEvent = origEvent.originalEvent;
			if (origEvent.type == 'keydown')
				$("#cbxPeriodo").click();
			$("#id_periodo_curso").val(ui.item.id);
			return false;
		}
	});	
	$("#cbxAlumno").autocomplete({
		source : '/admin/explorer/e_alumno',
		minLength : 1,
		change : function(ev, ui) {
			if (!ui.item) {
				$(this).val('');
			}
		},
		select : function(event, ui) {
			var origEvent = event;
			if (origEvent.type == 'autocompleteselect') {
				$("#cbxAlumno").val(ui.item.value);
			}
			while (origEvent.originalEvent !== undefined)
				origEvent = origEvent.originalEvent;
			if (origEvent.type == 'keydown')
				$("#cbxAlumno").click();

			$("#id_alumno").val(ui.item.id);
			return false;
		}
	});
});

function limpiar() {
	$(':input', '#frmInforme').not(':button, :submit, :reset, :hidden').val('')
			.removeAttr('checked').removeAttr('selected');
}

function generarPdf() {
	document.frmInforme.action = "/admin/gestionAlumnos/generar_reporte";
	document.frmInforme.method = "get";
	document.frmInforme.target = "_blank";
	document.frmInforme.submit();
}

function generarXls() {
	document.frmInforme.action = "/admin/gestionAlumnos/generar_reporte_csv";
	document.frmInforme.method = "get";
	document.frmInforme.target = "_blank";
	document.frmInforme.submit();

}
