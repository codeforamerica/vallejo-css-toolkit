$(document).ready(function(){
    $('#calls-nav-tab').addClass('active');

    $(".to-delete-submit-btn").hide();

    $(".clickable-cell").click(function(e) {
        if ($(this).data("href") !== undefined) {
            window.document.location = $(this).data("href");
        }
    });

    $("th").click(function() {
        if ($(this).data("href") !== undefined) {
            window.document.location = $(this).data("href");
        }
    });

    $(".to-delete-checkbox").click(function() {
        var any_checked = false,
            checkboxes = $(".to-delete-checkbox");
        for (i=0; i < checkboxes.length; i++) {
            is_checked = checkboxes[i].checked;
            if (is_checked) {
                any_checked = true;
                break;
            }
        }
        if (any_checked) {
            $(".to-delete-submit-btn").show();
        } else {
            $(".to-delete-submit-btn").hide();
        }
    });
});