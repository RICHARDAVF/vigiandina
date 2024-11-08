$(function(){
    var table = new DataTable('#data',{
        responsive:false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        paging:true,
        lengthChange: true, 
        autoWidth: false,
        destroy: true,
        searching: true, 
        deferRender: true,
        pageLength: 10, 
        dom:'Qfrtip',
        "order": [[0, 'desc']],
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
        columnDefs: [
            { "width": "5%", "targets": 0 }, 
            { "width": "10%", "targets": 1 },
            { "width": "35%", "targets": 2 },
            { "width": "35%", "targets": 3 },
            { "width": "15%", "targets": 4 },
            
        ],
        initComplete: function (settings, json) {
           
            new $.fn.dataTable.Buttons(table, {
                buttons: [
                    {
                        text:'<i class="fas fa-plus"></i>Nuevo registro',
                        action:function(e,dt,node,conf){
                            window.location.href = '/erp/empresa/add/'
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
    }
    )

})