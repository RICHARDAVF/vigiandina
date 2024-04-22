
$(document).ready(function() {
    var table = new DataTable('#data', {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',
        },
        dom: 'Qfrtip',
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
        initComplete: function (settings, json) {
           
           new $.fn.dataTable.Buttons(table, {
               buttons: [
                   'copy', 'excel', 'csv', 'pdf', 'print',
                   {
                    text:'Regresar',
                    action:function(){
                        history.back()
                    }
                   },
                   'pageLength',
   
               ],
               
               dom: {
                   button: {
                       className: 'btn btn-primary'
                   }
               }
           });

           // Crear un contenedor para los botones de exportación
           var $exportButtonsContainer = $('<div class="export-buttons-container"></div>');
           table.buttons().container().appendTo($exportButtonsContainer);

           // Agregar el contenedor de botones antes del input de búsqueda
           $exportButtonsContainer.insertBefore($('#data_wrapper .dataTables_filter'));
       }
    } );
   
});
