$(document).ready(function(){

    L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    var m = L.mapbox.map('map', 'mapbox.streets')
    .setView([38.113056, -122.235833], 13);

    var report_ids = JSON.parse(document.forms['report-ids']['report-ids'].value);
    for (i=0; i < report_ids.length; i++) {
        $.ajax({
            'url': '/workflow/geocode_address',
            'type': 'GET',
            'data': {
                'report_id': report_ids[i]
            }
        }).done(function (data) {
            if (data.lat && data.lon) {
                var marker = L.marker([data.lat, data.lon]);
                marker.addTo(m);
            }
        });
    }

    // load css data...
    // $.ajax({url: "/workflow/css_data", success: function(objs){
    //     for (i=0; i<objs.results.length; i++) {
    //         var circle = L.marker([objs.results[i].lat, objs.results[i].lng]);
    //         circle.addTo(m);
    //     }
    // }});

});