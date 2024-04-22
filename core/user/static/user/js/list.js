$(function () {
    var table = new DataTable('#data',{
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        // scrollX:true,
        dom:'Qfrtip',
   
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
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
            {"data": "full_name"},
            {"data": "username"},
            {"data": "dni"},
            {"data": "email"},
            {"data": "is_superuser"},     
            {"data": "image"},     
            {"data": "groups"},     
            {"data": "id"},
          
        ],
        columnDefs: [
            
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (is_superuser=='True') {
                        return `<a href="/user/usuario/perms/${row.id}/">${row.username}</a>`;
                    }else {
                        return data;
                    }
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return `<span class='badge badge-success'>${row.is_superuser?'Administrador':'usuario'}</span>`;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.groups, function (key, value) {
                        html += '<span class="badge badge-success">' + value.name + '</span> ';
                    });
                    return html;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<div class="d-flex justify-content-center"> <a href="/user/usuario/update/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/user/usuario/delete/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a> </div>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
           
            new $.fn.dataTable.Buttons(table, {
                buttons: [
                    {
                        text:'<i class="fas fa-plus"></i>Nuevo registro',
                        action:function(e,dt,node,conf){
                            window.location.href = '/user/usuario/create'
                        }
                    },
                    'copy', 'excel', 'csv', 'pdf', 'print','pageLength'
    
                ],
                
            });

            // Crear un contenedor para los botones de exportación
            var $exportButtonsContainer = $('<div class="export-buttons-container"></div>');
            table.buttons().container().appendTo($exportButtonsContainer);

            // Agregar el contenedor de botones antes del input de búsqueda
            $exportButtonsContainer.insertBefore($('#data_wrapper .dataTables_filter'));
        }
    });
});