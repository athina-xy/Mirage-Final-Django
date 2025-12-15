// Controls the "Enter the Store" hero 

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
window.addEventListener("load", function () {
    const cartForms = document.querySelectorAll(".add-to-cart-form");

    cartForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();  

            const button = form.querySelector(".btn-buy");
            if (!button) return;

            // If this button has already added its item, do nothing
            if (button.dataset.inCart === "true") {
                return;
            }

            const formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                credentials: "same-origin"
            })
                .then(function () {
                    // Change text + colour
                    button.textContent = "Added 🛒";
                    if (button.classList.contains("btn-warning")) {
                        button.classList.remove("btn-warning");
                        button.classList.add("btn-success");
                    }

                    // Mark as in cart & disable 
                    button.dataset.inCart = "true";
                    button.disabled = true;

                    // cart badge
                    const cartBtn = document.querySelector(".floating-cart-btn");
                    if (cartBtn) {
                        let badge = cartBtn.querySelector(".floating-cart-badge");

                        if (!badge) {
                            // create the badge element
                            badge = document.createElement("span");
                            badge.className = "floating-cart-badge";
                            badge.textContent = "1";
                            cartBtn.appendChild(badge);
                        } else {
                            // Increment the existing count
                            const current = parseInt(badge.textContent || "0", 10) || 0;
                            badge.textContent = current + 1;
                        }
                    }
                })
                .catch(function (error) {
                    console.error("Error adding to cart:", error);
                });
        });
    });
});
