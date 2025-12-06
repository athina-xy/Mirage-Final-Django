// making the reveal animation 
document.addEventListener("DOMContentLoaded", function () {
    const enterBtn = document.getElementById("enterStoreBtn");
    const catalogue = document.getElementById("catalogueSection");

    if (!enterBtn || !catalogue) {
        return;
    }

    enterBtn.addEventListener("click", function (event) {
        event.preventDefault();

        // Reveal catalogue
        catalogue.classList.remove("catalogue-hidden");

        // Smooth scroll to it
        catalogue.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });
});
