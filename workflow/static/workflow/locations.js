$(document).ready(function(){

    $('#data-table').dataTable( {
        "ajax": {
            "url": "/workflow/locations_data",
            "dataSrc": "results"
        }

    } );


});