$(function(){
    const options = {
        hour:"2-digit",
        minute:"2-digit",
       
        hour12:false
    }
    const date = (new Date()).toLocaleTimeString("es-Es",options)
    $('#id_h_inicio').val(date)
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
                    
                    const name = $('#id_nombre');
                    const last_name = $('#id_apellidos');
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
        var tipo_documento = $("#id_tipo_documento").val();
        if(parseInt(tipo_documento)==1 && value.length==8){
            searchDNI(value)
        }else{
            $('#id_nombre').val('')
            $('#id_apellidos').val('')
        }
    });

    $('#id_estado').on('change',function(){
        const estado = $(this).val()
        const hora_inicio = $('#id_h_inicio').val()
        if(estado==2){
            $('#id_h_llegada').val(hora_inicio)
        }
        
    })
    $("#id_documento_empresa").on("keydown",function(e){
        if(e.key=='Enter'){
            e.preventDefault()
            var value  = $("#id_documento_empresa").val()
            $.ajax({
                url:window.location.pathname,
                type:"POST",
                dataType:"json",
                data:{
                    "action":"search_doc_empresa",
                    "documento":value
                },
                success:function(data){
                    if(data.error){
                        return alert(data.error)
                    }
       
                    $("#id_empresa").val(data.empresa)
                },
                error:function(xhr,status,error){
                    alert(`${status}:${error}`)
                }
            })
        }
    })
    $("#search_documento_empresa").on("click",function(){
       
        var value  = $("#id_documento_empresa").val()
        $.ajax({
            url:window.location.pathname,
            type:"POST",
            dataType:"json",
            data:{
                "action":"search_doc_empresa",
                "documento":value
            },
            success:function(data){
                if(data.error){
                    return alert(data.error)
                }
    
                $("#id_empresa").val(data.empresa)
            },
            error:function(xhr,status,error){
                alert(`${status}:${error}`)
            }
        })
        
    })
})
