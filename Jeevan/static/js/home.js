const carousalWrapper = document.querySelector(".carousal-wrapper")
const carousalItems = carousalWrapper.children;
function pauseCarousalSpin() {
    for (let i = 0; i < carousalItems.length; i++) {
        if (carousalItems[i].style.animationPlayState === "" || carousalItems[i].style.animationPlayState === "running") {
            carousalItems[i].style.animationPlayState = "paused"
        }
        else {
            carousalItems[i].style.animationPlayState = "running";
        }
    }
}

carousalWrapper.addEventListener('click', (event) => {
    pauseCarousalSpin()
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
