$(document).ready(function() {
    var min = new Date().getFullYear();
        max = min + 20;
        select = document.getElementById('cbxAnio');

    for (var i = min; i<=max; i++){
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = i;
        select.appendChild(opt);
    }

    select.value = new Date().getFullYear();
});