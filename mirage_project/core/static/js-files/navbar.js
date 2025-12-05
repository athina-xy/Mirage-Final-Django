$(function () {
    // Get the file name of current page
    let current = location.pathname.split("/").pop();

    // Remove active from all nav links (prevents duplicates)
    $(".nav-link").removeClass("active");

    // Add active to the matching link
    $(".nav-link").each(function () {
        if ($(this).attr("href") === current) {
            $(this).addClass("active");
        }
    });
});
