$(document).ready(function(){

    // $.ajax({url: "/workflow/locations_data", success: function(data){
    //     console.log(data);
    //     for (i=0; i<data.results.length; i++) {

    //         $("#data-table").append(
    //             "<tr><td>" + data.results[i][0] +
    //             "</td><td>" + data.results[i][1] +
    //             "</td></tr>"
    //         );
    //     }
    // }});

    $('#data-table').dataTable( {
        "ajax": {
            "url": "/workflow/locations_data",
            "dataSrc": "results"
        }

    } );


});