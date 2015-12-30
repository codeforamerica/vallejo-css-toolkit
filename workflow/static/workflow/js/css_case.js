function removeAssignee (e, tableCell, assignee) {
    e.preventDefault();
    $.ajax({
        "url": "/workflow/remove_case_assignee/",
        "type": "POST",
        "data": {"assignee": assignee, "case_id": document.forms['case-details-form']['case_id'].value},
    }).done( function() {
        tableCell.remove();
    });
}

function addActivity() {
    console.log('hi');

    $.ajax({
        // TODO update and support url
        // TODO need to link to existing to read them
        "url": "/workflow/add_contact_action/",
        "type": "POST",
        "data": {
            "date": document.forms['add_case_activity']['date'].value,
            "time": document.forms['add_case_activity']['time'].value,
            "time_spent": document.forms['add_case_activity']['time_spent'].value,
            "officer": document.forms['add_case_activity']['officer'].value,
            "description": document.forms['add_case_activity']['description'].value,
            "prop_secured": document.forms['add_case_activity']['prop_secured'].value,
            "boardup_co": document.forms['add_case_activity']['boardup_co'].value,
            "per1_name": document.forms['add_case_activity']['per1_name'].value,
            "per1_dob": document.forms['add_case_activity']['per1_dob'].value,
            "per2_name": document.forms['add_case_activity']['per2_name'].value,
            "per2_dob": document.forms['add_case_activity']['per2_dob'].value,
            "case-number": document.forms['add_case_activity']['case_number'].value,
        }
    }).done( function(data) {
        // TODO: update this
        // if ($('#call-log tr').length > 1) {
        //     $('#call-log tr:last').after('<tr><td>' + data.timestamp + '</td><td>' + data.contacter_name + '</td><td>' + data.contact_type + '</td><td>' + data.contact_description + '</td></tr>');
        // } else {
        //     $('#no-contacts-msg').hide();
        //     $('#call-log').find('tbody').append('<tr><td>' + data.timestamp + '</td><td>' + data.contacter_name + '</td><td>' + data.contact_type + '</td><td>' + data.contact_description + '</td></tr>');
        // }
        $('#addincident').modal('hide');
    });



}

$(document).ready(function(){

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

    $(".tab-pane").hide();
    $("#case-details").show();
    $(".pane-selectors a").click(function (e) {
        e.preventDefault();
        $(".list-group-item").removeClass("active");
        $(this).addClass("active");
        var paneId =  $(this).attr('href');
        $(".tab-pane").hide();
        $(paneId).show();
    });

    $("#add-assignee-submit").click(function (e) {
        e.preventDefault();
        var assignee = document.forms['case-details-form']['assignee_add'].value;
        if (assignee !== "") {
            $.ajax({
                "url": "/workflow/add_case_assignee/",
                "type": "POST",
                "data": {
                    "assignee": assignee,
                    "case_id": document.forms['case-details-form']['case_id'].value
                },
            }).done( function() {
                // var onclickString = "removeAssignee(event, this.parentElement, '" + assignee + "')";
                var tableCellString = "<td class='assignee-row-cell'>" + assignee + '&nbsp&nbsp&nbsp<a class="unassign" onclick="' +
                                        "removeAssignee(event, this.parentElement, '" + assignee + "')" +
                                        '" href="#"><i class="fa fa-close"></i></a></td>';
                var newCell = $(tableCellString);
                newCell.appendTo("#case-assignees");
                document.forms['case-details-form']['assignee_add'].value = "";
            });
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

    $.ajax({
        'url': '/workflow/get_case_assignees'
    }).done(function (data) {
        var userList = data.users;

        $('#assignee-selector .typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'users',
            source: substringMatcher(userList)
        });

    });

});
