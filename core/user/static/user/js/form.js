$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
        placeholder: 'Buscar...'
    });
   function searchDNI(dni){
    const url = window.location.pathname,
    data = {dni:dni,action:'searchdni'};
    
    $.ajax({
        url:url,
        type:'POST',
        dataType:'json',
        data:data,
        success:function(result){
            if(result.error){
                message_error(result.error)
            }else{
                const name = $('#id_first_name');
                const last_name = $('#id_last_name');
                name.val(result.data.nombres)
                last_name.val(`${result.data.apellido_paterno} ${result.data.apellido_materno}`)
            }
        },
        error:function(result){
           message_error(result.error)
        }

    });
   }
   const dni = $('#id_dni');
   dni.on('input',function(event){
    const value = event.target.value.trim();
   
    if(value!=='' && value.length===8){
        searchDNI(value)
    }else{
        $('#id_first_name').val('')
        $('#id_last_name').val('')
    }
   })
});