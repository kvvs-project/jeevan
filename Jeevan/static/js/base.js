document.addEventListener("DOMContentLoaded", () => {

    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");
    const navTitle = document.querySelector(".nav-title");

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
    navTitle.classList.remove('scrolled');
    window.addEventListener('scroll', (event) => {

        if (Math.round(window.scrollY) > window.innerHeight) {
            navTitle.classList.add('scrolled');
        } else {
            navTitle.classList.remove('scrolled');
        }
    });
});