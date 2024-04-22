
$(function(){
    var unidad = $('select[name="unidad"]');
    var puesto = $('select[name="puesto"]');
    $('.select2').select2({
        theme:'bootstrap4',
        languaje:'es',
        // placeholder:'Buscar...'
    });
    $('select[name="empresa"]').on("change",function(){
        var id = $(this).val();
        if(id===''){
            return -1
        }

        var  options = "<option value=''>--------------</option>";
        $.ajax({
            type:'POST',
            url : window.location.pathname,
            data:{
                "action":'search_unidad',
                "id":id
            },
            success:function(data){
                if(data.error){
                    return alert(data.error)
                }
                for(item in data){
                    options+=`<option value='${data[item].id}'>${data[item].unidad}</option>`
                }
                unidad.html(options)
            },
            error:function(error){
                alert(error)
            }
        })
    })
    $('select[name="unidad"]').on("change",function(){
        var id = $(this).val();
        if(id==''){
            return -1
        }
        var options = "<option value=''>----------</option>"
        $.ajax({
            type:'POST',
            url:window.location.pathname,
            data:{
                "action":'search_puesto',
                "id":id
            },
            success:function(data){
                if(data.error){
                    return alert(data.error)
                }
                for(item in data){
                    options+=`<option value='${data[item].id}'>${data[item].puesto}</option>`
                }
                puesto.html(options)
            },
            error:function(error){
                alert(error)
            }
        });
    })

});