const navTitle = document.querySelector(".nav-title");
const allSkeleton = document.querySelectorAll('.skeleton')
const allRedSkeleton = document.querySelectorAll('.skeleton-red')

navTitle.classList.add('scrolled');

// show the skeleton animation until elements are loaded
window.addEventListener('load', function() {
    allSkeleton.forEach(item => {
        item.classList.remove('skeleton')
    });
    allRedSkeleton.forEach(item => {
        item.classList.remove('skeleton-red')
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");
    let isMenuOpenedByHamburger = false;

    // hide the menu if there is no nav items
    if (navLinks.childElementCount == 0) {
        hamburger.style.display = "none" 
    }

    function closeMenuOnClickOutside(event) {
        const isClickInside = navLinks.contains(event.target);

        // if click is outside the menu and the menu if open then close the menu
        if (!isClickInside && navLinks.classList.contains('show') && isMenuOpenedByHamburger) {
            navLinks.classList.remove('show');
            hamburger.classList.toggle('opened');
            isMenuOpenedByHamburger = false;
            document.removeEventListener('click', closeMenuOnClickOutside);
        }
    }

    hamburger.addEventListener('click', (event) => {
        event.stopPropagation();
        navLinks.classList.toggle('show');
        hamburger.classList.toggle('opened');
        hamburger.setAttribute('aria-expanded', hamburger.classList.contains('opened'));

        // check if the menu is open to add close menu listener else remove the listener
        if (navLinks.classList.contains('show')) {
            isMenuOpenedByHamburger = true;
            document.addEventListener('click', closeMenuOnClickOutside);
        } else {
            isMenuOpenedByHamburger = false;
            document.removeEventListener('click', closeMenuOnClickOutside);
        }
    });
});
