$(function(){
    $(document).on('input','#id_ruc',function(){
        var ruc = $(this).val().trim()
        if(ruc.length==11){
            $.ajax({
                type:'POST',
                url:window.location.pathname,
                dataType:'json',
                data:{
                    "action":"search_ruc",
                    "ruc":ruc
                },
                success:function(data){
                   
                    if(data.error){
                       message_error(data.error)
                    }
                 
                    $('#id_razon_social').val(data.data.nombre_o_razon_social)
                    $('#id_direccion').val(data.data.direccion_completa)
                },
                error:function(result){
                    message_error(result.error)
                }
            })
        }
    })
})