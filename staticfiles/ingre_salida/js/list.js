
$(function(){

    var table = new DataTable('#data',{
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        "order": [[0, 'desc']],
        autoWidth:false,
        scrollX:true,
        destroy:true,
        deferRender:true,
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
        dom:'Qfrtip',
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
        ajax:{
            url:window.location.pathname,
            type:'POST',
            data:(d)=>{
                d.action = "searchdata",
                d.desde = $('#desde').val();
                d.hasta = $('#hasta').val();
            },
            dataSrc:''
        },
        columns:[
            {"data":"id"},
            {"data":"documento"},
            {"data":"nombres"},
            {"data":"empresa"},
            {"data":"fecha_ingreso"},
            {"data":"hora_ingreso"},
            {"data":"fecha_salida"},
            {"data":"hora_salida"},
            {"data":"placa"},
            {"data":"n_parqueo"},
            {"data":"motivo"},
            {"data":"id"},
           
        ],
        columnDefs:[
            {
                targets:[2],
                class:'rext-center',
                render:function(date,type,row){
                    
                    return `<div style="width:250px;">${date}</div>`;
                }
            },
            {
                targets:[3],
                class:'rext-center',
                render:function(date,type,row){
                    
                    return `<div style="width:150px;" class="text-truncate">${date}</div>`;
                }
            },
            {
                targets:[4],
                class:'text-center',
                render:function(date,type,row){
                    console.log(date)
                    return date
                }
            },
            {
                targets:[7],
                class:'rext-center',
                render:function(date,type,row){
                    var hora_salida  = date
                    if(hora_salida==null){
                        hora_salida = `<button class="btn btn-secondary btn-sm" id="hora_salida">MARCAR</button>`
                    }
                    return hora_salida;
                }
            },
            {
                targets:[-3],
                class:'rext-center',
                render:function(date,type,row){
                    var n_parqueo  = date
                    if(n_parqueo==null && row.placa!=null){
                        n_parqueo = `<button class="btn btn-secondary btn-sm" id="n_parqueo">REGISTRAR</button>`
                    }
                    return n_parqueo;
                }
            },
            {
                targets:[-1],
                class:'rext-center',
                render:function(date,type,row){
              

                    var buttons = '<div class="d-flex justify-content-center"><a href="/erp/ingsal/edit/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/ingsal/delete/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a></row>';
                    buttons+='<a href="/erp/ingsal/audi/'+row.id+'/" type="button" class="btn btn-primary btn-sm"><i class="fas fa-search"></i></a></div>';
                    
                    return buttons;
                   
                }
            },
        ],
        initComplete:function(settings,json){
            new $.fn.dataTable.Buttons(table,{
                buttons:[
                    {
                        text:'<i class="fas fa-plus"></i>Nuevo registro',
                        action:function(e,dt,node,conf){
                            window.location.href = '/erp/ingsal/add/'
                        }
                    },
                    'copy','excel',"csv","pdf",'pageLength'
                ],
                
            });
            var $exportButtonsContainer = $('<div class="export-buttons-container"></div>');
            table.buttons().container().appendTo($exportButtonsContainer);

            // Agregar el contenedor de botones antes del input de búsqueda
            $exportButtonsContainer.insertBefore($('#data_wrapper .dataTables_filter'));
            var desde = $('<label for="desde" class="ml-1">Desde </label><input id="desde" name="desde" type="date" class="form-control form-control-sm" style="height:30px;" />')
            var hasta = $('<label for="desde" class="ml-1">Hasta </label><input id="hasta" name="hasta" type="date" class="form-control form-control-sm" style="height:30px;" />')
            $('#data_filter').append(desde)
            $('#data_filter').append(hasta)
        
           
        }
    });

    $(document).on('click','#hora_salida',function(){
        var rowIndex = table.row($(this).closest('tr')).index();
        var id = table.cell(rowIndex,0).data();
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
                            type:'POST',
                            url:window.location.pathname,
                            dataType:'json',
                            data:{
                                "id":id,
                                "action":"confirm_hora_salida",
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
    $(document).on('change','#hasta', function() {
        table.ajax.reload();
    });


    const contenidoModal = ()=>{
        return (`
                <div class="modal fade" id="miModal" tabindex="-1" role="dialog" aria-labelledby="miModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="miModalLabel">Numero de Parqueo</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                            
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-success " id="btn_park_submit">GUARDAR</button>
                                <button type="button" class="btn btn-danger" data-dismiss="modal">CERRAR</button>
                            </div>
                        </div>
                    </div>
                </div>
    
                    `)};
    function showpark(){
            var rowIndex = table.row($(this).closest('tr')).index();
            var id = table.cell(rowIndex, 0).data();        
            $("body").append(contenidoModal);
            $('.modal-body').html(
                ` <form method="POST" action="." enctype="multipart/form-data" id="myForm">
                    <div class="d-flex justify-content-around mt-1">
                        <label class="form-label" style="width:50px;">ID: </label><input class="form-control ml-3" value="${id}" readonly="true" id="id" name="id"/>
                    </div>
                    <div class="d-flex justify-content-around mt-1">
                        <label class="form-label" style="width:50px;">Numero: </label><input type="text" class="form-control ml-3" id="n_park" name="n_park" />
                    </div>

                <form>
                `
            );
                    
            
            // Agrega el contenido del modal al cuerpo de la página
            // Activa el modal utilizando la función modal() de Bootstrap
            $("#miModal").modal("show");
        }
    $(document).on('click','#n_parqueo',showpark)

    $(document).on('click','#btn_park_submit',function(){
        var parking = $('#n_park').val()
        var id = $('#id').val()
        if(parking==''){
            return alert('Ingrese un numero de parqueo')
        }
        $.ajax({
            method:'POST',
            url:window.location.pathname,
            dataType:'json',
            data:{
                "action":"n_parkin",
                "parqueo":parking,
                "id":id
            },
            success:function(data){
                window.location.reload()
                if(data.error){
                    return alert(data.error)
                }
            },
            error:function(error){
                alert(error)
            }
        })
    })
    })