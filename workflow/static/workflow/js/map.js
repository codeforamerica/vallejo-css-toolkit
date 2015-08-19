$(document).ready(function(){

    $.fn.bootstrapSwitch.defaults.size = 'small';
    $("[name='css']").bootstrapSwitch();
    $("[name='scf']").bootstrapSwitch();
    $("[name='crw']").bootstrapSwitch();
    $("[name='rms']").bootstrapSwitch();

    var m = L.map("map").setView([38.113056, -122.235833], 13);
    L.tileLayer("http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.jpg",{minZoom:4,maxZoom:18,opacity:0.75,attribution:'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
    .addTo(m);

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