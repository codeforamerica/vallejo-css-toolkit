$(document).ready(function(){

    $('#cases-nav-tab').addClass('active');

    var table = $('#data-table').dataTable( {
        "iDisplayLength": 25,
        "processing": true,
        "bLengthChange": false,
        "serverSide": true,
        "ajax": "/workflow/cases_data",
        "order": [[ 0, "asc" ]],
        "columnDefs": [
            {
                "targets": [ 0 ],  // address w/ link
                "visible": true,
                "searchable": false,
                "orderData": [ 5 ]
            },
            {
                "targets": [ 1 ],  // raw_id
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 4 ],  // status
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 5 ],  // full address
                "visible": false,
                "searchable": true
            },
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