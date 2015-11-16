function addContact() {
    $.ajax({
        "url": "/workflow/add_contact_action/",
        "type": "POST",
        "data": {
            "verification_id": document.forms['add_contact_form']['verification_id'].value,
            "contacter_name": document.forms['add_contact_form']['contacter_name'].value,
            "contact_type": document.forms['add_contact_form']['contact_type'].value,
            "contact_description": document.forms['add_contact_form']['contact_description'].value,
        },
    }).done( function(data) {
        if ($('#call-log tr').length > 1) {
            $('#call-log tr:last').after('<tr><td>' + data.timestamp + '</td><td>' + data.contacter_name + '</td><td>' + data.contact_type + '</td><td>' + data.contact_description + '</td></tr>');
        } else {
            $('#no-contacts-msg').hide();
            $('#call-log').find('tbody').append('<tr><td>' + data.timestamp + '</td><td>' + data.contacter_name + '</td><td>' + data.contact_type + '</td><td>' + data.contact_description + '</td></tr>');
        }
        $('#addcontact').modal('hide');
    });
}

$(document).ready(function(){

    $(".tab-pane").hide();
    $("#prop-details").show();
    $(".pane-selectors a").click(function (e) {
        e.preventDefault();
        $(".list-group-item").removeClass("active");
        $(this).addClass("active");
        var paneId =  $(this).attr('href');
        $(".tab-pane").hide();
        $(paneId).show();
    });

    L.mapbox.accessToken = 'pk.eyJ1IjoiYWRzY2huZWlkZXIiLCJhIjoiSlcxbGd0NCJ9.9iU2iiEVRUSxpiQXkV_zFg';
    var m = L.mapbox.map('map', 'mapbox.streets')
        .setView([38.113056, -122.235833], 12);

    $.ajax({
        'url': '/workflow/geocode_address',
        'type': 'GET',
        'data': {
            'report_id': document.forms['property-details-form']['report_id'].value
        }
    }).done(function (data) {
        if (data.lat && data.lon) {
            var marker = L.marker([data.lat, data.lon]);
            marker.addTo(m);
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
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

});
