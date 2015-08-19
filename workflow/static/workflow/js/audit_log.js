$(document).ready(function(){

    $.ajax({url: "/workflow/call_audit_log_data", success: function(data){

        for (i=0; i<data.results.length; i++) {

            $("#data-table").append(
                "<tr><td>" + "<a href='/workflow/call/" + data.results[i].id + "'>" + data.results[i].caller_number + "</a>" +
                "</td><td>" + data.results[i].first_name + " " + data.results[i].last_name +
                "</td><td>" + data.results[i].timestamp +
                "</td><td>" + data.results[i].changed_field +
                "</td><td>" + data.results[i].old_value +
                "</td><td>" + data.results[i].new_value +
                "</td></tr>"
            );
        }
    }});

});