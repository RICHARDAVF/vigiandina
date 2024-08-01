$(function(){
    var codigo_value = '';
    
    $("#codigo_rfid").on("keypress", function(e){
        if (e.which === 13) { // 13 es el código de la tecla Enter
            codigo_value = $(this).val().trim();
            $(this).attr("readonly", true); // Desactivar el input
            console.log('Código RFID:', codigo_value);

            // Simular una operación asincrónica como enviar a la base de datos
            setTimeout(() => {
                // Aquí puedes agregar la lógica para enviar el código RFID a la base de datos
                // Si la operación es exitosa o falla, reactivar el input
                $(this).attr("readonly", false);
                $(this).val(''); // Limpiar el input después de procesar el valor
            }, 2000);
        }
    });
});
