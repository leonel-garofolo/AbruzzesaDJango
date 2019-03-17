$(document).ready(function() {
    $(".field-id_caja").css({'visibility': 'hidden'});
    $("#btnImprimir").click(function(){            
        $('#pdf-iframe').attr("src", '/admin/function/comprobante?id_caja=' + $(".readonly").text()).load(function(){
            document.getElementById('pdf-iframe').contentWindow.print();
        });        
	});
});