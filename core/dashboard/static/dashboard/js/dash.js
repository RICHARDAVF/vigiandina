function pet_ajax(fecha_hora){
    $.ajax({
        type: 'POST',
        url: window.location.pathname,
        dataType: 'json',
        data: {
            "action": "dash",
            "fecha_hora":fecha_hora
        },
        success: function(data) {
            if (data.error) {
                return alert(data.error);
            }
            var tableBody = $('#data-body');
            tableBody.empty();
            
            for (var i = 0; i < data.length; i++) {
                var item = data[i];
                console.log(item)
                var row = $('<tr>');
                row.append($('<td>').text(item.id));
                row.append($('<td>').text(`${item.nombre} ${item.apellidos}`));
                row.append($('<td>').text(item.fecha));
                row.append($('<td>').text(item.h_inicio));
                row.append($('<td>').text(item.sala));
                tableBody.append(row);
            }
        },
        error: function() {
           
        }
    });
}
$(function(){
    var fecha_hora = $('#fecha_hora').val()
    pet_ajax(fecha_hora)});
$(document).on('change','#fecha_hora',function(){
    var fecha_hora = $(this).val()
    pet_ajax(fecha_hora)
})
$(document).on("click","#btn-report",function(){

    // var parameters = new FormData($("form"))
    alert("Mensaje:Funcion en desarrollo, espere la siguiente actualizacion")
    // $.ajax({
    //     method:"POST",
    //     url:"/dashboard/pdf/report-1/",
    //     dataType:"json",
    //     data:function(d){
    //         d.action = "report"
    //         d.desde = $("desde").val()
    //         d.hasta = $("hasta").val()
    //     },
    //     success:function(data){
    //         console.log("suce")
    //     }
    // })
})