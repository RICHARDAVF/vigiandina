$(function() {

    function load_table(data){
        $("#data-list").DataTable({
            data: data,
            destroy: true,
            columns: [
                { title: "ID", data: "id" },
                { title: "Trabajador", data: 'nombre' },
                { title: 'Hora Ingreso', data: 'hora_ingreso' },
                { title: "Hora Salida", data: 'hora_salida' },
                { title: "Fecha", data: 'fecha' }
            ]
        });
    }

    var codigo = '';
    var timeID = null;
    var resetCodigoTimeoutID = null;

    function valid() {
     
        if (timeID) {
            clearTimeout(timeID);
        }
    
        timeID = setTimeout(() => {
            $('#codigo_rfid').attr("readonly", false);
            $('#codigo_rfid').val('');
            $('#codigo_rfid').focus();
        }, 1000);
    }
    function resetCodigoAfterInactivity() {
       
        if (resetCodigoTimeoutID) {
            clearTimeout(resetCodigoTimeoutID);
        }
        resetCodigoTimeoutID = setTimeout(() => {
            codigo = '';
        }, 5000);
    }

    $('#codigo_rfid').on('keypress', function(e) {
        if (e.which === 13) {
            e.preventDefault(); 
            var currentCode = $(this).val().trim();
            if (codigo !== currentCode) {
                codigo = currentCode;
                $(this).attr("readonly", true);
                var form = new FormData(document.getElementById('create-form'));
                $.ajax({
                    type: "POST",
                    url: window.location.pathname,
                    data: form,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        load_table(JSON.parse(response));
                        valid();
                        resetCodigoAfterInactivity();
                    },
                    error: function(xhr, status, error) {
                        valid();
                        resetCodigoAfterInactivity();
                    }
                });
            } else {
                valid();
                resetCodigoAfterInactivity();
            }
        } else {
            resetCodigoAfterInactivity(); 
        }
    });

    load_table(data);
    $('#codigo_rfid').focus();

});
