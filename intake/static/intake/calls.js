$(document).ready(function(){

    var table = $('#data-table').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": "/intake/calls_data",
        "columnDefs": [
            {
                "targets": [ 6 ],  // filtered count
                "visible": false,
                "searchable": false
            }
        ]
    } );

});