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
        if(value.trim()===''){
            return
        }
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
    $("#search_trabajador").on("click",function(){
        var dni = $("#id_dni").val()
        var nombre = $("#id_nombre").val()
        var apellidos = $("#id_apellidos").val()
        var datos = {"action":"search_trabajador"}
        if(dni.trim()!=''){
            datos["key"]="nro_documento"
            datos["value"]=dni
        }else if(nombre.trim()!=''){
            datos["key"] = "nombres"
            datos["value"] = nombre

        }else if(apellidos.trim()!=''){
            datos["key"]= "nombres"
            datos["value"] = apellidos

        }else{
            return false
        }

        $.ajax({
            url:'/erp/trab/list/',
            type:"POST",
            data:datos,
            dataType:'json',
            success:function(data){
                if(data.error){
                    return alert(data.error)
                }
                $(".modal-body").empty()
                var items = `
                <table class="table table-striped  table-hover w-100 table" id="data-2">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Apellido</th>
                            <th>Documento</th>
                            <th>Opcion</th>
                        </tr>
                    </thead>
                    <tbody>
                    `
                for(item of data){
                   items+=`
                    <tr>
                        <td>${item.nombre}</td>
                        <td>${item.apellidos}</td>
                        <td>${item.documento}</td>
                        <td class="text-center">
                            <a rel='add' class="fas fa-plus"></a>
                        </td>
                    </tr>
                   `
                }
                items+='</tbody></table>'
                
                var modal = $("#exampleModal")
                var modal_body = modal.find(".modal-body")
                modal_body.html(items)
                modal.modal("show")
                $("#data-2 tbody").on("click","a[rel='add']",function(){
                    var tr = $(this).closest("tr","li")
                    var td = tr.find("td")
                    var dates  = []
                    td.each(function(){
                        dates.push($(this).text())
                    })
                    $("#id_dni").val(dates[2])
                    $("#id_nombre").val(dates[0])
                    $("#id_apellidos").val(dates[1])
                    $("#exampleModal").modal("hide")
                })

            },
            error:function(xhr,status,error){
                console.log(xhr.responseTxt)
            }
        })
    })
})

