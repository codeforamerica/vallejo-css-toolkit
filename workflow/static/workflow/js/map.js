$(document).ready(function(){

    $.fn.bootstrapSwitch.defaults.size = 'small';
    $("[name='css']").bootstrapSwitch();
    $("[name='scf']").bootstrapSwitch();
    $("[name='crw']").bootstrapSwitch();
    $("[name='rms']").bootstrapSwitch();

    // var layer = new L.StamenTileLayer("toner-lite");
    // var m = new L.Map("map", {
    //     center: new L.LatLng(38.113056, -122.235833),
    //     zoom: 13
    // });
    // m.addLayer(layer);

    L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    var m = L.mapbox.map('map', 'mapbox.light')
        .setView([38.113056, -122.235833], 13);

    // load see click fix data via api...
    $.ajax({url: "https://seeclickfix.com/api/v2/issues/?place_url=vallejo&per_page=100", success: function(result){
        for (i=0; i<result.issues.length; i++) {
            var circle = L.circle([result.issues[i].lat, result.issues[i].lng], 100, {
                color: '#0033CC',
                fillColor: '#0099FF',
                fillOpacity: 0.5,
                stroke: false
            }).addTo(m);
        }
    }});

    // load css data...
    $.ajax({url: "/workflow/css_data", success: function(objs){
        for (i=0; i<objs.results.length; i++) {
            var circle = L.circle([objs.results[i].lat, objs.results[i].lng], 100, {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.5,
                stroke: false
            }).addTo(m);
        }
    }});

    // load pd rims data...
    $.ajax({url: "/workflow/rms_data", success: function(objs){
        for (i=0; i<objs.results.length; i++) {
            var circle = L.circle([objs.results[i].lat, objs.results[i].lng], 100, {
                color: '#006600',
                fillColor: '#009933',
                fillOpacity: 0.5,
                stroke: false
            }).addTo(m);
        }
    }});
});