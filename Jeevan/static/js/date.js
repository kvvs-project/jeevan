const daysContainer = document.querySelector('.days');
const monthSelect = document.querySelector('.month-select');
const yearSelect = document.querySelector('.year-select');
const calendar = document.querySelector('.calendar');
const inputWrapper = document.getElementById('input-wrapper');
const dateInput = document.getElementById('date-input');

let currentMonth = 0; // Start with January
const currentYear = new Date().getFullYear(); // Get the current year
const maxYear = parseInt(inputWrapper.getAttribute('data-max')) || currentYear; // Default to current year if data-max is missing
const minYear = parseInt(inputWrapper.getAttribute('data-min')) || (currentYear - 125); // Default to currentYear - 125 if data-min is missing

// Set the initial year to the max year
let year = maxYear;

// Populate month and year custom dropdowns
function populateDropdowns() {
    const monthOptions = monthSelect.querySelector('.custom-options');
    monthOptions.innerHTML = '';
    for (let m = 0; m < 12; m++) {
        const option = document.createElement('div');
        option.className = 'custom-option';
        option.textContent = new Date(0, m).toLocaleString('default', { month: 'long' });
        option.dataset.value = m;
        monthOptions.appendChild(option);
    }

    const yearOptions = yearSelect.querySelector('.custom-options');
    yearOptions.innerHTML = '';
    for (let y = maxYear; y >= minYear; y--) {
        const option = document.createElement('div');
        option.className = 'custom-option';
        option.textContent = y;
        option.dataset.value = y;
        yearOptions.appendChild(option);
    }

    monthSelect.querySelector('.select-trigger').textContent = new Date(0, currentMonth).toLocaleString('default', { month: 'long' });
    yearSelect.querySelector('.select-trigger').textContent = year;
}

function generateCalendar(month, year) {
    daysContainer.innerHTML = '';

    const firstDay = new Date(year, month).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
        daysContainer.innerHTML += '<div></div>'; // Empty days for alignment
    }

    for (let date = 1; date <= lastDate; date++) {
        daysContainer.innerHTML += `<div>${date}</div>`;
    }
}

// Initial call
populateDropdowns();
generateCalendar(currentMonth, year);

// Show calendar on button click
dateInput.addEventListener('click', () => {
    calendar.style.display = calendar.style.display === 'flex' ? 'none' : 'flex';
});

// Handle month selection
monthSelect.querySelector('.custom-options').addEventListener('click', (e) => {
    if (e.target.classList.contains('custom-option')) {
        currentMonth = parseInt(e.target.dataset.value);
        monthSelect.querySelector('.select-trigger').textContent = e.target.textContent;
        generateCalendar(currentMonth, year);
        closeCustomSelects();
    }
});

// Handle year selection
yearSelect.querySelector('.custom-options').addEventListener('click', (e) => {
    if (e.target.classList.contains('custom-option')) {
        year = parseInt(e.target.dataset.value);
        yearSelect.querySelector('.select-trigger').textContent = e.target.textContent;
        generateCalendar(currentMonth, year);
        closeCustomSelects();
    }
});

// Handle day selection
daysContainer.addEventListener('click', (e) => {
    if (e.target.textContent) {
        const selectedDay = e.target.textContent.padStart(2, '0'); // Pad single digits
        const selectedMonth = (currentMonth + 1).toString().padStart(2, '0'); // Month is 0-indexed
        const selectedYear = year;

        const formattedDate = `${selectedYear}-${selectedMonth}-${selectedDay}`;
        dateInput.value = formattedDate; // Set the input value to formatted date
        calendar.style.display = 'none'; // Hide calendar after selection
    }
});

// Close custom select menus
function closeCustomSelects() {
    document.querySelectorAll('.custom-options').forEach(options => {
        options.style.display = 'none';
    });
}

// Toggle custom select menu
document.querySelectorAll('.custom-select').forEach(select => {
    select.querySelector('.select-trigger').addEventListener('click', () => {
        const options = select.querySelector('.custom-options');
        options.style.display = options.style.display === 'block' ? 'none' : 'block';
        closeCustomSelects();
        options.style.display = 'block'; // Show only the clicked one
    });
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-select') && !e.target.closest('.date-button')) {
        closeCustomSelects();
    }
});

// Initialize the dropdown values
monthSelect.querySelector('.select-trigger').textContent = new Date(0, currentMonth).toLocaleString('default', { month: 'long' });
yearSelect.querySelector('.select-trigger').textContent = year;
