$(document).ready(function(){

    $('#calls-nav-tab').addClass('active');

    var table = $('#data-table').dataTable( {
        "iDisplayLength": 25,
        "processing": true,
        "bLengthChange": false,
        "serverSide": true,
        "ajax": "/workflow/reports_data",
        "order": [[ 2, "desc" ]],
        "columnDefs": [
            {
                "targets": [ 0 ],  // id
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 1 ],  // reported_datetime
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 2 ],  // reported_datetime_link
                "visible": true,
                "searchable": false,
                "orderData": [ 1 ]
            },
            {
                "targets": [ 3 ],  // caller_name
                "visible": false,
                "searchable": true
            },
            {
                "targets": [ 4 ],  // caller_name_link
                "visible": true,
                "searchable": false,
                "orderData": [ 3 ]
            },
            {
                "targets": [ 5 ],  // caller_number
                "visible": false,
                "searchable": true
            },
            {
                "targets": [ 6 ],  // caller_number_link
                "visible": false,
                "searchable": false,
                "orderData": [ 5 ]
            },
            {
                "targets": [ 7 ],  // problem_address
                "visible": false,
                "searchable": true
            },
            {
                "targets": [ 8 ],  // problem_address_link
                "visible": true,
                "searchable": false,
                "orderData": [ 7 ]
            },
            {
                "targets": [ 9 ],  // status
                "visible": false,
                "searchable": true
            },
            {
                "targets": [ 10 ],  // status_link
                "visible": true,
                "searchable": false,
                "orderData": [ 9 ]
            },
            {
                "targets": [ 11 ],  // resolution
                "visible": false,
                "searchable": true
            },
            {
                "targets": [ 12 ],  // resolution_link
                "visible": true,
                "searchable": false,
                "orderData": [ 11 ]
            },
            {
                "targets": [ 13 ],  // filtered count
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 14 ],  // total count
                "visible": false,
                "searchable": false
            }
        ]
    } );

});