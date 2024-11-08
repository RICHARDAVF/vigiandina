$(function(){
    var table = new $('#data').DataTable({
        language:{
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
        dom:'Qfrtip',
        initComplete: function (settings, json) {
           
            new $.fn.dataTable.Buttons(table, {
                buttons: [
                    {
                        text:'<i class="fas fa-plus"></i>Nuevo registro',
                        action:function(e,dt,node,conf){
                            window.location.href = '/erp/area/trabajo/add/'
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
    })
})