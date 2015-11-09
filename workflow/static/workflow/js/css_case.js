function removeAssignee (e, tableCell, assignee) {
    e.preventDefault();
    $.ajax({
        "url": "/workflow/remove_case_assignee/",
        "type": "POST",
        "data": {"assignee": assignee, "case_id": $("#case_id").val()},
    }).done( function() {
        tableCell.remove();
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
        var assignee = $("#case-details-form")[0][7].value;
        if (assignee !== "") {
            $.ajax({
                "url": "/workflow/add_case_assignee/",
                "type": "POST",
                "data": {"assignee": assignee, "case_id": $("#case_id").val()},
            }).done( function() {
                // var onclickString = "removeAssignee(event, this.parentElement, '" + assignee + "')";
                var tableCellString = "<td class='assignee-row-cell'>" + assignee + '&nbsp&nbsp&nbsp<a class="unassign" onclick="' +
                                        "removeAssignee(event, this.parentElement, '" + assignee + "')" +
                                        '" href="#"><i class="fa fa-close"></i></a></td>';
                var newCell = $(tableCellString);
                newCell.appendTo("#case-assignees");
                $("#case-details-form")[0][6].value = "";
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

    // TODO: get these names and departments from the db:
    var userList = ['Ofc. Hans Williams (CSS)', 'Cpl. John Garcia (CSS)', 'Eli Flushman (CAO)'];

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
