$(document).ready(function(){

    $("#notifications").click(function markSeen() {
        $(".new_notification_count").addClass('seen');
        $(".new_notification_bell").addClass('seen');

        // $.ajax({
        //     url: "/mark_notifications_seen/"
        // });

    });

    $.ajax({
        url: "/get_notifications/",
        success: function(result){
            if (result.notifications.length === 0) {
                $(".new_notification_count").addClass('seen');
                $(".new_notification_bell").addClass('seen');
            } else {
                $(".new_notification_count").text('(' + result.notifications.length + ')');

                $(".notification-details").addClass("dropdown-menu");
                for (i=0; i<result.notifications.length; i++) {
                    $(".notification-details").append('<li><a href="/workflow/report/' + result.notifications[i].report_id + '">' + result.notifications[i].message + '</a></li>');
                }
            }
        }
    });

});