const navTitle = document.querySelector(".nav-title");
navTitle.classList.add('scrolled');

document.addEventListener("DOMContentLoaded", () => {

    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    function closeMenuOnClickOutside(event) {
        const isClickInside = navLinks.contains(event.target);

        if (!isClickInside && navLinks.classList.contains('show')) {
            navLinks.classList.remove('show');
            hamburger.classList.toggle('opened');
        }
    }
    document.addEventListener('click', closeMenuOnClickOutside);
    
    hamburger.addEventListener('click', (event) => {
        event.stopPropagation();
        navLinks.classList.toggle('show');
        hamburger.classList.toggle('opened');
        hamburger.setAttribute('aria-expanded', hamburger.classList.contains('opened'));
    });
});