$(document).ready(function(){

    $('#calls-nav-tab').addClass('active');

    var table = $('#data-table').dataTable( {
        "iDisplayLength": 25,
        "processing": true,
        "serverSide": true,
        "ajax": "/workflow/calls_data",
        "order": [[ 0, "desc" ]],
        "columnDefs": [
            {
                "targets": [ 0 ],  // id w/ link
                "visible": true,
                "searchable": false,
                "orderData": [ 7 ]
            },
            {
                "targets": [ 7 ],  // raw id
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 8 ],  // filtered count
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 9 ],  // total count
                "visible": false,
                "searchable": false
            }
        ]
    } );

});