$(document).ready(function(){

    // var map = L.map('map').setView([38.102381, -122.2601924], 13);
    // L.tileLayer("http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.jpg",{minZoom:4,maxZoom:18,opacity:0.75,attribution:'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'})
    // .addTo(map);

    // L.marker([38.102381, -122.2601924]).addTo(map);

    // L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    // var m = L.mapbox.map('map', 'mapbox.streets')
    //     .setView([38.102381, -122.2601924], 13);


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // constructs the suggestion engine
    var substringMatcher = function(strs) {
        return function findMatches(q, cb) {
            var matches, substringRegex;

            // an array that will be populated with substring matches
            matches = [];

            // regex used to determine if a string contains the substring `q`
            substrRegex = new RegExp(q, 'i');

            // iterate through the pool of strings and for any string that
            // contains the substring `q`, add it to the `matches` array
            $.each(strs, function(i, str) {
                if (substrRegex.test(str)) {
                    matches.push(str);
                }
            });

            cb(matches);
        };
    };

    // $.ajax({
    //     url: 'workflow/street_names.json',
    //     type: 'get',
    //     dataType: 'json',
    //     error: function(data){
    //         console.log(data);
    //     },
    //     success: function(data){

    //         $('#reporter-street-name-selector .typeahead').typeahead({
    //             hint: true,
    //             highlight: true,
    //             minLength: 3
    //         },
    //         {
    //             name: 'streets',
    //             source: substringMatcher(data)
    //         });
    //     }
    // });


            $('#reporter-street-name-selector .typeahead').typeahead({
                hint: true,
                highlight: true,
                minLength: 3
            },
            {
                name: 'streets',
                source: substringMatcher(streetNames)
            });











});