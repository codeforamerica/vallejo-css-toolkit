$(document).ready(function(){

    // var map = L.map('map').setView([38.102381, -122.2601924], 13);
    // L.tileLayer("http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.jpg",{minZoom:4,maxZoom:18,opacity:0.75,attribution:'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
    // .addTo(map);

    // L.marker([38.102381, -122.2601924]).addTo(map);

    L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    var m = L.mapbox.map('map', 'mapbox.streets')
        .setView([38.102381, -122.2601924], 13);

});