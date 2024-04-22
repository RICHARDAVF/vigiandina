$(function () {
    var miTabla = $('#data').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
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
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "numero"},
            {"data": "nombre"},
            {"data": "estado"},
            {"data": "id"},
        ],
        columnDefs:[
            {
                targets:[3],
                class:'rext-center',
                render:function(date,type,row){
                    var state = 'LIBRE'
                    if(!row.estado){
                        state = 'OCUPADO'
                    }
                   return '<div><strong>'+state+'</strong></div>'
                }
            },
            {
                targets:[-1],
                class:'rext-center',
                render:function(date,type,row){
                    var buttons = '<div class="d-flex justify-content-center"><a href="/erp/parqueo/update/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/parqueo/delete/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a></row>';
                    return buttons;
                }
            },
        ],

        initComplete: function (settings, json) {
            // Habilitar los botones de exportación
            new $.fn.dataTable.Buttons(miTabla, {
                buttons: [
                    {
                        text:'<i class="fas fa-plus"></i>Nuevo registro',
                        action:function(e,dt,node,conf){
                            window.location.href = '/erp/parqueo/create/'
                        }
                    },
                    'copy', 'excel', 'csv', 'pdf', 'print','pageLength'
                ],
                // Personalizar la apariencia de los botones (opcional)
                
            });

            // Crear un contenedor para los botones de exportación
            var $exportButtonsContainer = $('<div class="export-buttons-container"></div>');
            miTabla.buttons().container().appendTo($exportButtonsContainer);

            // Agregar el contenedor de botones antes del input de búsqueda
            $exportButtonsContainer.insertBefore($('#data_wrapper .dataTables_filter'));
        }
    });
});