$(function () {
    var action = $('#id_action').val()
    if(action!='edit'){

        $('#btn-cancel').css('display', 'none')
    }
    $('#id_motivo').val('LABORAR')
    $('.select2').select2({
        theme: 'bootstrap4',
        tags:true,
        allowClear:true,

        placeholder: 'Buscar Trabajador',
        ajax: {
            method: 'POST',
            url: '/erp/ingsal/list/',
            dataType: 'json',
            data: function (params) {
                var queryParams = {
                    q: params.term,
                    action: 'search_trabajador'
                }
                return queryParams
            },
            processResults: function (data, params) {
          
                params.page = params.page || 1;
                return {
                    results: data,
                    pagination: {
                        more: (params.page * 30 < data.total_count)
                    }
                };
            },
            
        },
        minimumInputLength: 1,
        language: 'es',
        templateResult: formatRepo,
        templateSelection: formatRepoSelection
    });
    const barcodeInput = $('<input type="text" id="hiddenBarcodeInput" style="position:absolute; left:-9999px;">');
    $('body').append(barcodeInput);
    function formatRepo(repo) {
        
        if (repo.loading) {
            return repo.text;
        }
        var container = $('<div class="select2-result"><div class="select2-nombre"></div></div>');
        container.find('.select2-nombre').text(repo.text);
        return container;
    }

    function formatRepoSelection(repo) {
        return repo.text;
    }
});
