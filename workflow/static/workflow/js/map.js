$(document).ready(function(){

    $('#props-nav-tab').addClass('active');

    $.fn.bootstrapSwitch.defaults.size = 'small';
    $("#cssCheckbox").bootstrapSwitch('state', true);
    $("[name='scf']").bootstrapSwitch();
    $("[name='crw']").bootstrapSwitch();
    $("[name='rms']").bootstrapSwitch();

    L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    var m = L.mapbox.map('map', 'mapbox.streets')
        .setView([38.113056, -122.235833], 13);

    var seeClickFixIssues = [];
    var rmsCases = [];
    var crwCases = [];
    var cssCases = [];

    // load see click fix data via api...
    $.ajax({url: "https://seeclickfix.com/api/v2/issues/?place_url=vallejo&per_page=100", success: function(result){
        for (i=0; i<result.issues.length; i++) {
            var circle = L.circle([result.issues[i].lat, result.issues[i].lng], 100, {
                color: '#0033CC',
                fillColor: '#0099FF',
                fillOpacity: 0.5,
                stroke: false
            });
            seeClickFixIssues.push(circle);
            if ($('input[name="scf"]')[0].checked === true) {
                circle.addTo(m);
            }
        }
    }});

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
            cssCases.push(circle);
            if (document.getElementById("cssCheckbox").checked === true) {
                circle.addTo(m);
            }
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
            });
            rmsCases.push(circle);
            if ($('input[name="rms"]')[0].checked === true) {
                circle.addTo(m);
            }
        }
    }});

    $('input[name="scf"]').on('switchChange.bootstrapSwitch', function(event, state) {
        if (state === false) {
            seeClickFixIssues.forEach(function(e) {
                m.removeLayer(e);
            });
        } else if (state === true) {
            seeClickFixIssues.forEach(function(e) {
                m.addLayer(e);
            });
        }
    });

    $("#cssCheckbox").on('switchChange.bootstrapSwitch', function(event, state) {
        if (state === false) {
            cssCases.forEach(function(e) {
                m.removeLayer(e);
            });
        } else if (state === true) {
            cssCases.forEach(function(e) {
                m.addLayer(e);
            });
        }
    });

    $('input[name="rms"]').on('switchChange.bootstrapSwitch', function(event, state) {
        if (state === false) {
            rmsCases.forEach(function(e) {
                m.removeLayer(e);
            });
        } else if (state === true) {
            rmsCases.forEach(function(e) {
                m.addLayer(e);
            });
        }
    });

    $('input[name="crw"]').on('switchChange.bootstrapSwitch', function(event, state) {
        if (state === false) {
            crwCases.forEach(function(e) {
                m.removeLayer(e);
            });
        } else if (state === true) {
            crwCases.forEach(function(e) {
                m.addLayer(e);
            });
        }
    });

});
