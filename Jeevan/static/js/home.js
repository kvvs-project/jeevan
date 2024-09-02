document.addEventListener("DOMContentLoaded", () => {

    const navTitle = document.querySelector(".nav-title");
    const carousalWrapper = document.querySelector(".carousal-wrapper")
    const carousalItems = document.querySelectorAll(".carousal-item")

    carousalWrapper.addEventListener('click', (event) => {
        carousalItems.forEach(element => {
            if (element.style.animationPlayState === "" || element.style.animationPlayState === "running") {
                element.style.animationPlayState = "paused"
            }
            else {
                element.style.animationPlayState = "running";
            }
        });
    });

    // enable service worker for pwa support
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/js/serviceWorker.js').then((registration) => {
                console.log('Service Worker registered with scope:', registration.scope);
            }).catch((err) => {
                console.log('Service Worker registration failed:', err);
            });
        });
    }

    navTitle.classList.remove('scrolled');
    window.addEventListener('scroll', (event) => {

        if (Math.round(window.scrollY) > window.innerHeight) {
            navTitle.classList.add('scrolled');
        } else {
            navTitle.classList.remove('scrolled');
        }
    });

});