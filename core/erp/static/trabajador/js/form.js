$(function(){
    function searchDNI(dni){
        const url = window.location.pathname
        const token = $("input[name='csrfmiddlewaretoken']").val()
        data = {dni:dni,action:'searchdni','csrfmiddlewaretoken':token};
        
        $.ajax({
            url:url,
            type:'POST',
            dataType:'json',
            data:data,
            success:function(result){
                if(result.error){
                    message_error(result.error)
                }else{
                    const nombre = $('#id_nombre');
                    const apellidos = $('#id_apellidos');
                    nombre.val(result.data.nombres)
                    apellidos.val(`${result.data.apellido_paterno} ${result.data.apellido_materno}`)
                }
            },
            error:function(result){
               message_error(result.error)
            }
    
        });
       }
    const dni = $('#id_documento');

    dni.on('input',function(event){
    const value = event.target.value.trim();
   
    if(value!=='' && value.length===8){
        searchDNI(value)
    }else{
        $('#id_nombre').val('')
        $('#id_apellidos').val('')
    }
   })
   $('.select2').select2({
    theme:'bootstrap4',
    language:'es',
    placeholder:'buscar...'
   })
});