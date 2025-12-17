// NOT USED ANYMORE - KEEPING FOR REFERENCE 


//document.addEventListener("DOMContentLoaded", () => {
//  const btn = document.getElementById("enterStoreBtn");
//  const catalogue = document.getElementById("catalogueSection");

//  if (!catalogue) return

//  function openCatalogue(scroll = true) {
//    catalogue.classList.remove("catalogue-hidden");
//    catalogue.style.display = ""; // clear any inline "display:none" if it exists

//    if (scroll) {
//      setTimeout(() => {
//        catalogue.scrollIntoView({ behavior: "smooth", block: "start" });
//      }, 30);
//    }
//  }

  // Button opens catalogue
//  if (btn) {
//    btn.addEventListener("click", (e) => {
//      e.preventDefault();
//      openCatalogue(true);
 //   });
//  }

  // If user comes from navbar link "/#catalogueSection"
 // if (window.location.hash === "#catalogueSection") {
 //   openCatalogue(true);
 // }

  // If user used filters/search, auto-open catalogue (so results show)
 // const hasQueryParams = window.location.search && window.location.search.length > 1;
 // if (hasQueryParams) {
  //  openCatalogue(true);
 // }

  // If hash changes later (rare, but nice)
 // window.addEventListener("hashchange", () => {
  //  if (window.location.hash === "#catalogueSection") {
//      openCatalogue(true);
//    }
 // });
// });