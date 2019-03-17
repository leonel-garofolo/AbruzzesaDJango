$(document).ready(function() {
	$(".datepicker").datepicker({
		dateFormat : 'dd/mm/yy'
	});

	$("#cbxConcepto").autocomplete({
		source : '/admin/explorer/e_concepto',
		minLength : 1,
		change : function(ev, ui) {
			if (!ui.item) {
				$(this).val('');
			}
		},
		select : function(event, ui) {
			var origEvent = event;
			if (origEvent.type == 'autocompleteselect') {
				$("#cbxConcepto").val(ui.item.value);
			}
			while (origEvent.originalEvent !== undefined)
				origEvent = origEvent.originalEvent;
			if (origEvent.type == 'keydown')
				$("#cbxConcepto").click();
			$("#id_concepto").val(ui.item.id);
			return false;
		}
	});
});

function limpiar() {
	$(':input', '#frmInforme').not(':button, :submit, :reset, :hidden').val('')
			.removeAttr('checked').removeAttr('selected');
}