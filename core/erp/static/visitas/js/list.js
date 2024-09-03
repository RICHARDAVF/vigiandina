$(function () {
    var miTabla = new DataTable('#data',{
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        "order": [[0, 'desc']],
        responsive: false,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        scrollX:true,
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
        dom:'Qfrtip',
        // fixedColumns:{
        //     left:3,
        //     // right:2
        // },
        conditions:{
            num:{
                'MultipleOf':{
                    conditionName:'MultipleOf',
                    init : function(that,fn,preDefined=null){
                        var el = $`<input/>`.on('input',function(){fn(that,this)});
                        if(preDefined!==null){
                            $(el).val(preDefined[0]);
                        }
                        return el
                    },
                    inputValue:function(el){
                        return $(el[0].val());
                    },
                    isInputValid:function(el,that){
                        return $(el[0].val().length!==0);
                    },
                    search:function(value,comparison){
                        return value%comparison===0;
                    }
                }
            }
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data:(d)=>{
                d.action = 'searchdata'
                d.desde = $("#desde").val()
                d.hasta = $("#hasta").val()

            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},//0
            {"data": "estado"},//1
            {"data": "names"},//2
            {"data": "fecha"},//3
            {"data": "h_inicio"},//4
            {"data":"fecha_salida"},//5
            {"data": "h_salida"},//6
            {"data": "dni"},//7
            {"data": "id"},//8
            {"data": "empresa"},//9
            {"data": "cargo"},//10
            {'data': "motivo"},//11
            {'data': "sala"},//12
            {'data': "sctr_salud"},//13
            {'data': "p_visita"},//14
            {'data': "documentos"},//15
            {'data': "id"},//16
            {'data': "id"},//17
            {'data': "id"},//18
        ],
        headerCallback: function (thead, data, start, end, display) {
            // Aplicar el fondo al encabezado de las tres primeras columnas
            $(thead).find('th').slice(0, 3).css('background-color', 'rgb(238, 137, 49)');
        },
        columnDefs:[
            {
                targets:[1],
                class:'text-center',
                render:function(data,type,row){
                    var opt = ''
                    if(row.estado==1){
                        opt = `<div style="display: flex; align-items: center;">
                        <strong class="bg-success" style="font-size:11px;border-radius:5px; padding:5px;">PROGRAMADO</strong>
                        <input class="btn btn-danger btn-sm" id="anular" type="button" value="ANULAR" style="font-size:11px;border-radius:5px; padding:5px;"/>
                    </div>`
                    }else if(row.estado==2){
                       
                        opt = ` 
                        <strong class="bg-success" style="font-size:11px;border-radius:5px; padding:5px;">EN CURSO</strong>
                            `
                    }else if(row.estado==3){
                        opt='<strong class="bg-success" style="font-size:11px;border-radius:5px; padding:5px;">FINALIZADO</strong>'
                    }else{
                        opt = '<strong class="bg-danger" style="font-size:11px;border-radius:5px; padding:5px;">ANULADO</strong>'
                    }
                   
                    return opt
                }
            },
            {
               
                class:'text-center',
                targets:[2],
                render:function(data,type,row){
                    return '<div style="width:250px;font-size:12px; font-weight: bold;">'+row.names+'</div>'
                }
            },
            {class:"text-center",targets:[3],render:function(data,type,row){
                return `<strong>${data}</strong>`
            }},
            {class:"text-center",targets:[4],render:function(data,type,row){
                return `<strong>${data}</strong>`
            }},
            {
                targets:[6],
                class:'text-center',
                render:function(data,type,row){
                    var hora = '<input type="button" value="Confirmar" id="h_salida" class="btn btn-secondary btn-sm">'
                    if(row.h_salida!==null){
                        hora = '<strong">'+data+'</strong>'
                    }
                    return hora
                }
            },
           

             
            {
               
                class:'text-center',
                targets:[8],
                render:function(data,type,row){
                    if(row.estado==0){
                        return '<strong>Anulado</strong>'
                    }
                   var date = (row.tipo==1)?`<input type='button' id='btnaddperson' class="btn btn-primary btn-sm" value='Asistente'/>`:'';
                    return date
                }
            },
            {
               
                class:'text-center',
                targets:[9],
                render:function(data,type,row){
                    var cargo = (row.cargo!=null)?row.cargo:"";
                    return '<div style="width:200px;"><strong style="width:font-size:13px;">'+cargo+'</strong></div>'
                }
            },
            {
               
                class:'text-center',
                targets:[10],
                render:function(data,type,row){
                    return '<div style="width:200px;" class="text-truncate">'+row.empresa+'</div>'
                }
            },
           
           
            {
                targets:[11],
                class:'text-center',
                render:function(data,type,row){
                    return '<div style="width:200px;"><strong style="font-size:13px;"">'+row.motivo+'</strong></div>'
                }
            },
            {
                targets:[13],
                class:'text-center',
                render:function(data,type,row){
                  
                    return `<a href='${data}' target="_blank" ><i class="fas fa-file-pdf bg-red"></i></a>`
                }
            },
            {
                targets:[14],
                class:'text-center',
                render:function(data,type,row){
                  
                    return `<div style="width:250px; font-weight: bold;font-size:12px;">${row.p_visita}</div>`
                }
            },
           
            {
                targets:[16],
                class:'text-center',
                render:function(data,type,row){
                    if(row.estado==0){
                        return '<strong>Anulado</strong>'
                    }
                    return '<input type="button" class="btn btn-warning btn-sm" value="info." id="addvehiculo"/>'
                }
            },
            {
                targets:[17],
                class:'text-center',
                render:function(data,type,row){
                    
                    return `<a class="btn btn-primary btn-sm" href="/erp/visita/ep/${row.id}/"><i class="fas fa-eye"></i></a>`
                }
            },
            {
                targets:[18],
                class:'text-center',
                render:function(data,type,row){
                    if(row.estado==0){
                        return '<strong>Anulado</strong>'
                    }
                    var part_url = 'visita/update/'
                    if(row.tipo==2){
                        part_url = 'delivery/update/'
                    }
                    var buttons = '<div class="d-flex justify-content-center"><a href="/erp/'+part_url + row.id + '/" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/visita/delete/' + row.id + '/" type="button" class="btn btn-danger btn-sm"><i class="fas fa-trash-alt"></i></a>'
                    buttons+='<a href="/erp/visita/audi/'+row.id+'/" type="button" class="btn btn-primary btn-sm"><i class="fas fa-search"></i></a></div>';
                    return buttons;
                }
            },
            

        ],
        createdRow: function (row, data, dataIndex) {
            
            if (data.estado==0) {
                $(row).find('td').css('background-color', '#f58d8d');
               
            }
        },
        initComplete: function (settings, json) {
          
            new $.fn.dataTable.Buttons(miTabla, {
                buttons: [
                    {
                        text:"<i class='fas fa-plus'></i> VISITA",
                        action:function ( e, dt, node, conf ) {
                            window.location.href = '/erp/visita/create/';
                        }
                    },
                    {
                        text:"<i class='fas fa-plus'></i> DELIVERY",
                        action:function ( e, dt, node, conf ) {
                            window.location.href = '/erp/delivery/create/';
                        }
                    },
                    {
                        text:"<i class='fas fa-plus'></i> TRABAJADOR",
                        action:function ( e, dt, node, conf ) {
                            window.location.href = '/erp/ingsal/add/';
                        }
                    },
                    
                    'copy',
                    'excel',
                    'csv',
                    {
                        extend: "pdf",
                        text: 'pdf',
                        orientation: "landscape", 
                        pageSize: "LEGAL", 
                        exportOptions: {
                          columns: ':visible',
                        }
                    },
                    'print',
                    'pageLength'
                    
                ],
               
                
            });

           
            var $exportButtonsContainer = $('<div class="export-buttons-container"></div>');
            miTabla.buttons().container().appendTo($exportButtonsContainer);

           
            $exportButtonsContainer.insertBefore($('#data_wrapper .dataTables_filter'));
           // Crear los campos "Desde" y "Hasta"
            var desde = $(`
                <div class="form-group mb-0 mr-1">
                    <label for="desde" class="mr-1">Desde:</label>
                    <input id="desde" name="desde" type="date" class="form-control form-control-sm" />
                </div>
            `);

            var hasta = $(`
                <div class="form-group mb-0 mr-1">
                    <label for="hasta" class="mr-1">Hasta:</label>
                    <input id="hasta" name="hasta" type="date" class="form-control form-control-sm" />
                </div>
            `);

            var selectOptions = $(`
                <div class='form-group mb-0 d-flex mr-1'>
                    <label class='mr-1' for='options'>Usuario:</label>
                    <select id="options-users" class="form-control form-control-sm" >
                        
                    </select>
                </div>
             
            `);



            // Asegúrate de que el contenedor se alinee a la derecha dentro de '#data_filter'
            $('#data_filter').addClass('d-flex justify-content-end');

            $('#data_filter').append(desde);
            $('#data_filter').append(hasta);
            $('#data_filter').append(selectOptions);
            $('#dropdownMenuButton').on("click",function(){
           
            })

            var select = $("#options-users")
            select.empty()
            select.append(new Option("-------","-1"))
            user_supervised.forEach(function(user){
                select.append(new Option(user.value,user.id))
            })
        }
    });
   $(document).on("change","#hasta",function(){
    miTabla.ajax.reload()
   })
    $('.btnTest').css('display','none')
    const contenidoModal = ()=>{
        return (`
                <div class="modal fade bd-example-modal-lg" id="miModal" tabindex="-1" role="dialog" aria-labelledby="miModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="miModalLabel">Personas en la reunion</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                            
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-danger" data-dismiss="modal">CERRAR</button>
                            </div>
                        </div>
                    </div>
                </div>
    
                    `)};

    var parqueos = []
    function listdates(datos){
        var tdhtml = ''
        
        for(item in datos){
            
            tdhtml+=`
            <tr>
                <td>${datos[item].id}</td>
                <td>${datos[item].documento}</td>
                <td>${datos[item].nombre}</td>
                <td>${datos[item].apellidos}</td>
                <td>${datos[item].empresa}</td>
                <td>${datos[item].marca_v}</td>
                <td>${datos[item].modelo_v}</td>
                <td>${datos[item].placa_v}</td>
                <td>${datos[item].soat_v}</td>
                
                <td>
                    <a href="${datos[item].sctr}" target="_blank">file</a></>
                </td>
           
                <td>
                    ${(datos[item].n_parqueo===null || datos[item].n_parqueo==undefined)?'':datos[item].n_parqueo}
                </td>
                <td>
                ${(datos[item].n_parqueo===null || datos[item].n_parqueo==undefined)?'':'<a type="button" class="btn btn-success btn-sm" id="hab_park">Hab.</a>'}

                </td>
            <tr>`
        }
        $('.table-group-divider').html(
            tdhtml
        )
        $('#documento').val('')
        $('#nombre').val('')
        $('#apellidos').val('')
        $('#apellido').val('')
        $('#empresa').val('')
        $('#modelo_v').val('')
        $('#placa_v').val('')
        $('#n_parqueo').val('')

    }
    function showperson(){
        var rowIndex = miTabla.row($(this).closest('tr')).index();
        var id = miTabla.cell(rowIndex,0).data();
        id_visita = id
        $.ajax({
            type:"POST",
            url:window.location.pathname,
            dataType:'json',
            data:{
                "id":id,
                "action":'addperson',
            },
            success:function(data){
                
                parqueos = data.parking
                var opt_select = '<select name="n_parqueo"  class="form-control ml-3"  id="n_parqueo">'
                for(var item of parqueos){
                    opt_select+=`
                    <option value="${item.id}" class="form-control">${item.numero}</option>
                `
                }
                opt_select+= "</select>"
               
                $('.modal-body').html(
                    ` <form  enctype="multipart/form-data" id="myForm">
                        <input type='hidden' class="form-control ml-3" value="${id}" editable='false' id="id" name="id"/>
                        <div class="mt-1  d-flex felx-row">
                            <label class="form-label ml-1">DNI: </label><input  class="form-control ml-3"  id="documento" name="documento" />
                            <label class="form-label">Nombre: </label><input class="form-control ml-3"   id="nombre" name="nombre"/>
                        </div>
                        <div class="mt-1  d-flex felx-row">
                            <label class="form-label ml-1">Apellidos: </label><input  class="form-control ml-3"  id="apellidos" name="apellidos" />
                            <label class="form-label">Empresa: </label><input  class="form-control ml-3"  id="empresa" name="empresa"/>
                        </div>
                        
                        <div class="mt-1  d-flex felx-row">
                            <label class="form-label ml-1">Marca: </label><input  class="form-control ml-3"  id="marca_v" name="marca_v"/>
                            <label class="form-label ml-1">Modelo: </label><input  class="form-control ml-3"  id="modelo_v" name="modelo_v"/>
                        </div>
                            
                        <div class="mt-1 d-flex felx-row">
                            <label class="form-label">Placa: </label><input  class="form-control ml-3"  id="placa_v" name="placa_v" />
                            <label class="form-label ml-1">FV-SOAT: </label><input  class="form-control ml-3" type='date'  id="soat_v" name="soat_v"  />
                        </div>
                        <div class="mt-1 d-flex felx-row">
                            <label class="form-label">SCTR: </label><input  class="form-control ml-3" type='file'  id="sctr" name="sctr" />
                            <label class="form-label ml-1">N° Parqueo: </label>${opt_select}
                        </div>
                    <form>
                    <a type='button' class='btn btn-primary mt-1 mb-1' id='addperson'><i class='fas fa-plus'></i>Agregar</a>
                    <div class="table-responsive">
                        <table class="table table-striped" id="id_asis">
                            <thead class="table-light">
                                <caption>Table Name</caption>
                                <tr>
                                    <th >#ID</th>
                                    <th >DNI</th>
                                    <th >NOMBRE</th>
                                    <th >APELLIDO</th>
                                    <th >EMPRESA</th>
                                    <th >MARCA</th>
                                    <th >MODELO</th>
                                    <th >PLACA</th>
                                    <th >SOAT</th>
                                    <th >SCTR</th>
                                    <th >PARQUEO</th>
                                    <th >OPCIONES</th>
                                </tr>
                                </thead>
                                <tbody class="table-group-divider">
                                
                                </tbody>
                                <tfoot>
                                    
                                </tfoot>
                        </table>
                    </div>


                    `
                );
                listdates(data.asis);
            },
            error:function(){
                alert("Error en la peticion")
            }
        });
        $('body').append(contenidoModal);
        $("#miModal").modal('show');
        
    }
    
    $(document).on("click","#btnaddperson",showperson);
   
    $(document).on('click', '#addperson', function () {
       
        var formData = new FormData($('#myForm')[0]);
        var vh = $('#marca_v').val()
        if(vh.length!=0){
            var park = $('#n_parqueo').val()
            if(park==null){
                return alert('Debe selccionar un parqueo')
            }
        }
        formData.append('action', 'addperson');
        $.ajax({
            type: 'POST',
            url: '/erp/visita/asis/add/',
            dataType: 'json',
            data: formData,
            processData: false, 
            contentType: false,
            success: function (data) {
          
               if(data.error){
                return alert(data.error)
               }
               
               
               listdates(data);
            },
            error: function (data) {
                alert(data.error);
            }
        });
    
        
    });
    
    $(document).on('input','#documento',function(event){
        const doc = $('#documento').val();
        $('#nombre').val('')
        $('#apellidos').val('')
        if (doc.trim().length==8){
            $.ajax({
                type:'POST',
                url:'/erp/visita/create/',
                dataType:'json',
                data:{
                    action:'searchdni',
                    dni:doc.trim(),
                },
                success:function(data){
                    if(data.error){
                        $('#nombre').val('')
                        $('#apellidos').val('')
                        return alert(data.error);
                    }
                
                    $('#nombre').val(`${data.data.nombres}`)
                    $('#apellidos').val(`${data.data.apellido_paterno} ${data.data.apellido_materno}`)
                   
                },
                error:function(data){
                    $('#nombre').val('')
                    $('#apellidos').val('')
                    alert(data.error)
                }
    
            })
        }
        
    })
    $(document).on('click',"#hora_llegada",function(){
        var rowIndex = miTabla.row($(this).closest('tr')).index();
        var id = miTabla.cell(rowIndex,0).data();
        $.confirm({
            theme: 'material',
            title: 'Alerta',
            icon: 'fas fa-info',
            content: "¿Esta seguro de marcar la hora de llegada?",
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons:{
                info:{
                    text:'Si',
                    btnClass:'btn-primary',
                    action:function(){
                        $.ajax({
                            type:'POST',
                            url:window.location.pathname,
                            dataType:'json',
                            data:{
                                "id":id,
                                "action":"confirm",
                            },
                            success:function(data){
                                window.location.reload()
                                if(data.error){
                                    return alert(data.error)
                                }
                              
                            },
                            error:function(){
                                alert("Hubo un error en la peticion")
                            }
                        })
                    }
                },
                danger:{
                    text:'No',
                    btnClass:'btn-red',
                    action:function(){

                    }
                }
            }
        })
        
    })
    $(document).on("click","#addvehiculo",function(){
        $('body').append(contenidoModal);
        var rowIndex = miTabla.row($(this).closest('tr')).index();
        var id = miTabla.cell(rowIndex,0).data();
        $.ajax({
            type:'POST',
            url:window.location.pathname,
            dataType:'json',
            data:{
                "id":id,
                "action":"addvh"
            },
            success:function(data){
               console.log(data)
                if(data.error){
                    return alert(data.error)
                }
                var opt = '<select class="form-control" id="num_park">'
                if(data.vh.n_parqueo==null){
                    opt+=`<option value="">-------</option>`
                    for(let item of  data.parking){
                        opt+=`<option value="${item.id}">${item.numero}</option>`
                    }
                }else{
                    opt+=`<option>${data.vh.n_parqueo}</option>`
                }
                
                opt+="</select>"
                $('.modal-body').html(
                    ` <form  enctype="multipart/form-data" id="FormVH">
                        <input type='hidden' class="form-control ml-3" value="${id}" editable='false' id="id" name="id"/>
                        <div class="mt-1">
                            <div class="d-flex">
                                <label class="form-label">Marca: </label><input class="form-control ml-4" ${(data.vh.v_marca!==null)?'value="'+data.vh.v_marca+'"':''}  id="v_marca" name="v_marca"/>
                            </div>
                            <div class="d-flex mt-2">
                                <label class="form-label">Modelo: </label><input  class="form-control ml-4 " ${(data.vh.v_modelo!==null)?'value="'+data.vh.v_modelo+'"':''}  id="v_modelo" name="v_modelo"/>
                            </div>
                            <div class="d-flex mt-2">
                                <label class="form-label">Placa: </label><input  class="form-control ml-4 " ${(data.vh.v_placa!==null)?'value="'+data.vh.v_placa+'"':''} id="v_placa" name="v_placa" />
                            </div>
                            <div class="d-flex mt-2">
                                <label class="form-label">FV-SOAT: </label><input  class="form-control ml-4 " ${(data.vh.fv_soat!=='None')?'value="'+data.vh.fv_soat+'"':''} id="fv_soat" name="fv_soat" type="date" />
                            </div>
                            <div class="d-flex mt-2">
                                <label class="form-label ml-1">N° Parqueo: </label>
                                ${opt}
                            </div>
                            <div class="d-flex mt-2">
                                <label class="form-label">Obervacion: </label><input  class="form-control ml-4 " ${(data.vh.observacion!==null)?'value="'+data.vh.observacion+'"':''} id="observacion" name="observacion" />
                            </div>
                        </div>
                        <input type="button" class="btn btn-success" value="GUARDAR" id="formvh"/>
                    <form>`
                )
                $('#miModal').modal('show')
            },
            error:function(){
                alert("Ocurrio un error")
            }
        })
        
    })
    $(document).on("click","#h_salida",function(){
        var rowIndex = miTabla.row($(this).closest('tr')).index();
        var id = miTabla.cell(rowIndex,0).data();
        $.confirm({
            theme: 'material',
            title: 'Alerta',
            icon: 'fas fa-info',
            content: "¿Esta seguro de marcar la hora de salida?",
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons:{
                info:{
                    text:'Si',
                    btnClass:'btn-primary',
                    action:function(){
                        $.ajax({
                            type:"POST",
                            url:window.location.pathname,
                            dataType:'json',
                            data:{
                                "id":id,
                                "action":"h_salida"
                            },
                            success:function(data){
                                window.location.reload()
                            },
                            error:function(jqXHR, textStatus, errorThrown){
                                alert("Error en la solicitud "+textStatus,errorThrown)
                            }
                        })
                    }
                },
                danger:{
                    text:'No',
                    btnClass:'btn-red',
                    action:function(){

                    }
                }
            }
        })
       
    })
    $(document).on("click","#anular",function(){
        var rowIndex = miTabla.row($(this).closest('tr')).index();
        var id = miTabla.cell(rowIndex,0).data();
        $.confirm({
            theme: 'material',
            title: 'Alerta',
            icon: 'fas fa-info',
            content: "¿Esta seguro de anular?",
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons:{
                info:{
                    text:'Si',
                    btnClass:'btn-primary',
                    action:function(){
                        $.ajax({
                            type:'POST',
                            url : window.location.pathname,
                            dataType:'json',
                            data:{
                                "id":id,
                                "action":'anular'
                            },
                            success:function(data){
                                if(data.error){
                                    return alert(data.error)
                                }
                                window.location.reload()
                            },
                            error:function(jqXHR, textStatus, errorThrown){
                                        alert("Error en la solicitud "+textStatus,errorThrown)
                                    }
                        })
                    }
                },
                danger:{
                    text:'No',
                    btnClass:'btn-red',
                    action:function(){

                    }
                }
            }
        })
    })
    $(document).on('click','#formvh',function(){
        const formData = new FormData($('#FormVH')[0])
        formData.append('action', 'formvh');
        formData.append('n_parqueo',$('#num_park').val() );
        
        $.ajax({
            type:'POST',
            dataType:'json',
            url:window.location.pathname,
            data:formData,
            processData: false, 
            contentType: false,
            success:function(data){
                if(data.error){
                    return alert(data.error)
                }
                window.location.reload()
            },
            error:function(jqXHR, textStatus, errorThrown){
                alert("Ocurrio un error ",textStatus,errorThrown)
                window.location.reload()
            }
        })
    })
    $(document).on('click','#hab_park',function(){
        var row = $(this).closest('tr');
        var id = row.find('td:first').text();
        $.ajax({
            type:'POST',
            url:'/erp/visita/asis/add/',
            dataType:'json',
            data:{
                "action":'lib_park',
                "id":id
            },
            success:function(data){
                if(data.error){
                    return alert(data.error)
                }
                window.location.reload()
            },
            error:function(){

            }
        })
        
    })
});

