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
        if (objs.results.length < 10) {
            var circle = L.marker([38.099047, -122.218044]);
            circle.addTo(m);

            var circle = L.marker([38.0881142, -122.2255658]);
            circle.addTo(m);

            var circle = L.marker([38.1104313, -122.2392161]);
            circle.addTo(m);

            var circle = L.marker([38.1092024, -122.2637288]);
            circle.addTo(m);

            var circle = L.marker([38.086010359999996, -122.22689059999999]);
            circle.addTo(m);

            var circle = L.marker([38.122789491666666, -122.23419952500001]);
            circle.addTo(m);

            var circle = L.marker([38.126071, -122.231788]);
            circle.addTo(m);

            var circle = L.marker([38.1235362, -122.2174162]);
            circle.addTo(m);

            var circle = L.marker([38.15007075, -122.22810015]);
            circle.addTo(m);

            var circle = L.marker([38.0997673, -122.23280475384615]);
            circle.addTo(m);
        }
    }});

});