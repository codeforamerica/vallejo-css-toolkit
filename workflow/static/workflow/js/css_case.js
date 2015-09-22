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

});