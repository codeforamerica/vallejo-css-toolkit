$(document).ready(function(){

    var statusMap = {null: '', 1: 'Unreviewed', 2: 'Active', 3: 'Closed', 4: 'Suspended'};

    $.ajax({url: "/intake/my_assignments_data", success: function(data){

        for (i=0; i<data.results.length; i++) {

            $("#data-table").append(
                "<tr><td>" + "<a href='/intake/call/" + data.results[i].id + "'>" + data.results[i].caller_number + "</a>" +
                "</td><td>" + data.results[i].call_time +
                "</td><td>" + data.results[i].caller_name +
                "</td><td>" + data.results[i].problem_address +
                "</td><td>" + statusMap[data.results[i].status] +
                "</td><td>" + data.results[i].last_updated +
                "</td></tr>"
            );
        }
    }})
});