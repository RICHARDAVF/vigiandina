$(function(){
    var table = new DataTable("#data",{
        language: {
                    url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json" 
                },
        dom:'Qfrtip',

        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10 filas', '25 filas', '50 filas', 'Todo' ]
        ],
        ajax:{
            url:window.location.pathname,
            type:"POST",
            data:(d)=>{
                d.action = "searchdata"
                d.cantidad = $("#cantidad").val() || 100
                d.desde = $("#desde").val()
                d.hasta = $("#hasta").val()
            },
            dataSrc:"",
            dataType:"json",
        },
        columns:[
            {"data":"placa"},
            {"data":"tipo_documento"},
            {"data":"nro_documento"},
            {"data":"nombres"},
            {"data":"empresa"},
            {"data":"fecha"},
            {"data":"hora_ingreso"},
            {"data":"hora_salida"},
            {"data":"motivo"},
            {"data":"numero_parkin"},
            {"data":"tipo"},
        ],
        columnDefs:[
            {
                targets:[1],
                render:(data,type,row)=>{
                    if(data==1){
                        return "DNI"
                    }else if(data==2){
                        return "C.E"
                    }else{
                        return "PAS."
                    }
                }
            },
            {
                targets:[10],
                render:(data,type,row)=>{

                    return data
                }
            }
        ],
        pageLength: 25, 
        initComplete:function(settings,json){
            
            var content = `
                        
                        <label class="mr-2">Desde:</label>
                        <input type="date" id="desde" name="desde"/>
                        <label class="mr-2">Hasta: </label>
                        <input type="date" id="hasta" name="hasta" />
                        <input type="button" class="bg-success" id="generate_report" value="refresh"/>
                        <label>
                            Cantidad:
                            <input type="number" id="cantidad" class="mr-1" value="100" placeholder="Cantidad a cargar">
                        </label>

                        `
            $('.dataTables_filter').prepend(content);
            new $.fn.dataTable.Buttons(table, {
                buttons: [
                    'copy', 'excel', 'csv', 'pdf', 'print','pageLength'
                ],

               
            });

            // Crear un contenedor para los botones de exportación
            var $exportButtonsContainer = $('<div class="export-buttons-container"></div>');
            table.buttons().container().appendTo($exportButtonsContainer);

            // Agregar el contenedor de botones antes del input de búsqueda
            $exportButtonsContainer.insertBefore($('#data_wrapper .dataTables_filter'));
            $("#cantidad").on("keyup",function(event){
                if(event.keyCode===13){
                    table.ajax.reload()
                }
            })
            $("#generate_report").on("click",function(){
                var desde = $("#desde").val()
                var hasta = $("#hasta").val()
                if(desde=='' || hasta==""){
                    return alert("Ingrese un rango de fecha valido")
                }
                table.ajax.reload()
                })

        }
    })
})

