$(document).ready(function(){

    $('#cases-nav-tab').addClass('active');

    var table = $('#data-table').dataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": "/workflow/cases_data",
        "columnDefs": [
            {
                "targets": [ 5 ],  // filtered count
                "visible": false,
                "searchable": false
            },
            {
                "targets": [ 6 ],  // total count
                "visible": false,
                "searchable": false
            }
        ]
    } );

});