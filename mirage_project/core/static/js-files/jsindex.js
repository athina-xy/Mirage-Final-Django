// Controls the "Enter the Store" hero and logo visibility 

document.addEventListener("DOMContentLoaded", function () {
    const enterBtn = document.getElementById("enterStoreBtn");
    const catalogue = document.getElementById("catalogueSection");
    const hero = document.querySelector(".mirage-hero");
    const logoBar = document.getElementById("mirageLogoBar");

    if (!catalogue) {
        return;
    }

    // Use sessionStorage so behaviour resets when the browser/tab is closed
    const STORAGE_KEY = "mirageStoreEntered";
    const hasEnteredBefore = sessionStorage.getItem(STORAGE_KEY) === "yes";

    function showCatalogueOnly() {
        catalogue.classList.remove("catalogue-hidden");
        if (hero) {
            hero.classList.add("mirage-hero-hidden");
        }
    }

    function scrollToCatalogue() {
        catalogue.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    if (hasEnteredBefore) {
        // show catalogue + logo, hide hero
        showCatalogueOnly();
        if (logoBar) {
            logoBar.style.display = "block";
        }
    } else {
        // First time in this browser/tab session:
        // show hero, hide catalogue + logo until button pressed
        if (hero) {
            hero.classList.remove("mirage-hero-hidden");
        }
        catalogue.classList.add("catalogue-hidden");
        if (logoBar) {
            logoBar.style.display = "none";
        }
    }

    // When user clicks "Enter the Store"
    if (enterBtn) {
        enterBtn.addEventListener("click", function (event) {
            event.preventDefault();

            showCatalogueOnly();
            scrollToCatalogue();

            if (logoBar) {
                logoBar.style.display = "block";
            }

            // Remember for this session (until tab is closed)
            sessionStorage.setItem(STORAGE_KEY, "yes");
        });
    }
});

// Change cart button after adding 
document.addEventListener("DOMContentLoaded", function () {
    const addButtons = document.querySelectorAll(".btn-buy");

    addButtons.forEach(function (btn) {
        btn.addEventListener("click", function (event) {
            const button = event.currentTarget;

            // Change text
            button.textContent = "Added 🛒";

            // change colour from warning to success
            if (button.classList.contains("btn-warning")) {
                button.classList.remove("btn-warning");
                button.classList.add("btn-success");
            }
        });
    });
});
