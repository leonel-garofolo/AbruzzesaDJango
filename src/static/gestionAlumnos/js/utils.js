function post(url, data){
	var response = null;
	$.ajax({
		type : "POST",
		url : url,
		data : data,
		success : function(json) {	
			console.log(json)
			response = json;
		}
	});
	
	return response;
}

function limpiar(form){
	$(':input', '#' + form).not(':button, :submit, :reset, :hidden').val('')
	.removeAttr('checked').removeAttr('selected');
}

/*
 * variableHidden: campo hidden q contiene el id del combo
 * campoCombo: Campo donde se visualiza el combo que realiza la busqueda
 * nombreExplorer: nombre del explorador que busca en el servidor
 */
function explorer(variableHidden, campoCombo, nombreExplorer){
	$('#' + campoCombo).autocomplete({
		source : '/admin/explorer/' + nombreExplorer,
		minLength : 1,
		change : function(ev, ui) {
			if (!ui.item) {
				$(this).val('');
			}
		},
		select : function(event, ui) {
			var origEvent = event;
			if (origEvent.type == 'autocompleteselect') {
				$('#' + campoCombo).val(ui.item.value);
			}
			while (origEvent.originalEvent !== undefined)
				origEvent = origEvent.originalEvent;
			if (origEvent.type == 'keydown')
				$('#' + campoCombo).click();
			$('#' + variableHidden).val(ui.item.id);
			return false;
		}
	});
}


function datatable(variableName, columnsData){
	 var table= $('#' + variableName).DataTable( {		 		 
	 	language: {
	 		"sProcessing":     "Procesando...",
	 	    "sLengthMenu":     "Mostrar _MENU_ registros",
	 	    "sZeroRecords":    "No se encontraron resultados",
	 	    "sEmptyTable":     "-Sin Datos-",
	 	    "sInfo":           "Registros de _START_ a _END_ de un total de _TOTAL_",
	 	    "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
	 	    "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
	 	    "sInfoPostFix":    "",
	 	    "sSearch":         "Buscar:",
	 	    "sUrl":            "",
	 	    "sInfoThousands":  ",",
	 	    "sLoadingRecords": "Cargando...",
	 	    "oPaginate": {
	 	        "sFirst":    "Primero",
	 	        "sLast":     "Último",
	 	        "sNext":     "Siguiente",
	 	        "sPrevious": "Anterior"
	 	    },
	 	    "oAria": {
	 	        "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
	 	        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
	 	    }
	    },
	    columns: [
            { mData:"dni", title: "Dni" },
            { mData:"apellido", title: "Apellido" },
            { mData:"nombre", title: "Nombre" }           
        ],
        "columnDefs": [{
            "defaultContent": "-",
            "targets": "_all"
          }],
        "scrollY":        "200px",
        "scrollCollapse": true,
        "paging":         false
    } );	
	 	
	$('#' + variableName + ' tbody').on( 'click', 'tr', function () {
	       $(this).toggleClass('selected');
	 } );
		
	return table;
}