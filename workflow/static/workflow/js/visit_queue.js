$(document).ready(function(){

    $('#props-nav-tab').addClass('active');

    var table = $('#data-table').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": "/workflow/visit_queue_data",
        "columnDefs": [
            {
                "targets": [ 6 ],  // filtered count
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 7 ],  // total count
                "visible": false,
                "searchable": false
            }
        ]
    } );

});