// theme.js

$(function () {
    // 1. Read saved theme or default to dark
    const saved = localStorage.getItem("theme") || "dark";
    const isDarkAtStart = (saved === "dark");

    // 2. Apply initial theme class on body
    $("body").toggleClass("dark-theme", isDarkAtStart);

    // 3. Sync the crystal switch + label
    $("#themeToggle").prop("checked", isDarkAtStart);
    $(".mode-text").text(isDarkAtStart ? "Dark" : "Light");

    // 4. When user toggles
    $("#themeToggle").on("change", function () {
        const isDark = $(this).is(":checked");

        // Toggle class on body
        $("body").toggleClass("dark-theme", isDark);

        // Save preference
        localStorage.setItem("theme", isDark ? "dark" : "light");

        // Update label
        $(".mode-text").text(isDark ? "Dark" : "Light");
    });
});
