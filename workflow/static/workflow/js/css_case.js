function removeAssignee (e, tableCell) {
    e.preventDefault();
    tableCell.remove();
};

$(document).ready(function(){

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
        var assignee = $("#case-details-form")[0][6].value;
        if (assignee != "") {
            var newCell = $("<td class='assignee-row-cell'>" + assignee + "&nbsp&nbsp&nbsp<a class='unassign' onclick='removeAssignee(event, this.parentElement)' href='#'><i class='fa fa-close'></i></a></td>");
            newCell.appendTo("#case-assignees");
            $("#case-details-form")[0][6].value = "";
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
