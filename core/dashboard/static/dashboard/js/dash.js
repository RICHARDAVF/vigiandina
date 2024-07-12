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
$(document).on("click", "#btn-report", function () {
    var desde = $("#desde").val();
    var hasta = $("#hasta").val();
    var empresa = $("#empresa").val()
    var tipo = $('#tipo-report').val()
    if(desde=="" || hasta=="" || empresa=='' || tipo==''){
      return alert("Complete los todos los campos")
    }
    fetch("/dashboard/pdf/reporte-1/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "report",
        desde: desde,
        hasta: hasta,
        empresa:empresa,
        tipo:tipo
      }),
    })
      .then(response => {
        if (response.ok) {
          // Check for response content type (ensure it's PDF)
          if (response.headers.get("Content-Type")?.includes("application/pdf")) {
            
            return response.blob(); // Get the PDF blob
          } else {
            throw new Error("Unexpected response content type");
          }
        } else {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob); // Create a temporary URL
        const link = document.createElement("a");
        link.href = url;
        window.open(link.href, '_blank');
      })
      .catch(error => {
        alert("An error occurred: " + error.message);
      });
  });