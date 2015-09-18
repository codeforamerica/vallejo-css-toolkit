$(document).ready(function(){

    L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    var m = L.mapbox.map('map', 'mapbox.streets')
    .setView([38.113056, -122.235833], 13);
    // load css data...
    $.ajax({url: "/workflow/css_data", success: function(objs){
        for (i=0; i<objs.results.length; i++) {
            // var circle = L.circle([objs.results[i].lat, objs.results[i].lng], 100, {
            //     color: 'red',
            //     fillColor: '#f03',
            //     fillOpacity: 0.5,
            //     stroke: false
            // });
            var circle = L.marker([objs.results[i].lat, objs.results[i].lng]);
            circle.addTo(m);
        }
    }});

});