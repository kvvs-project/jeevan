const userGraph = document.getElementById('user-chart');
const bloodGraph = document.getElementById('blood-donation-chart');
const organGraph = document.getElementById('organ-donation-chart');
const userDetails = document.getElementById("user-details")

const bloodDateList = document.querySelector(".blood-donation-stats").dataset.blood
const organDateList = document.querySelector(".organ-donation-stats").dataset.organ
const hospitalCount = document.querySelector(".user-count-stats").dataset.hospital
const donorCount = document.querySelector(".user-count-stats").dataset.donor
const patientCount = document.querySelector(".user-count-stats").dataset.patient

const today = new Date();
const lastSevenDaysOfBlood = [];
const lastSevenDaysOfOrgan = [];
const bloodData = JSON.parse(bloodDateList)
const organData = JSON.parse(organDateList)

for (let i = 6; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    const bloodFormattedDate = date.toISOString().split('T')[0];
    const organFormattedDate = date.toISOString().split('T')[0];
    lastSevenDaysOfBlood.push(bloodFormattedDate);
    lastSevenDaysOfOrgan.push(organFormattedDate);
}

const bloodDonationMap = new Map();
bloodData.forEach(entry => {
    bloodDonationMap.set(entry.date, parseInt(entry.value, 10));
});

const organDonationMap = new Map();
organData.forEach(entry => {
    organDonationMap.set(entry.date, parseInt(entry.value, 10));
});

const bloodFinalData = lastSevenDaysOfBlood.map(date => {
    const bloodFormattedDate = date.split('-').join(' - ');
    return {
        date: bloodFormattedDate,
        value: bloodDonationMap.get(date) || 0
    };
});

const organFinalData = lastSevenDaysOfOrgan.map(date => {
    const organFormattedDate = date.split('-').join(' - ');
    return {
        date: organFormattedDate,
        value: organDonationMap.get(date) || 0
    };
});

const bloodGraphLabels = bloodFinalData.map(item => item.date);
const bloodGraphData = bloodFinalData.map(item => item.value);
const organGraphLabels = organFinalData.map(item => item.date);
const organGraphData = organFinalData.map(item => item.value);

const bloodGraphContext = {
    type: 'line',
    data: {
        labels: bloodGraphLabels,
        datasets: [{
            label: 'Blood Donations',
            data: bloodGraphData,
            fill: false,
            borderColor: 'rgb(253, 0, 87)',
            tension: 0.1
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            y: {
                suggestedMax: 10,
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        }
    }
}

const drawBloodChart = new Chart(bloodGraph, bloodGraphContext);

const organGraphContext = {
    type: 'line',
    data: {
        labels: organGraphLabels,
        datasets: [{
            label: 'Organ Donations',
            data: organGraphData,
            fill: false,
            borderColor: 'rgba(0, 94, 255, 0.396)',
            tension: 0.1
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            y: {
                suggestedMax: 10,
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        }
    }
}

const drawOrganChart = new Chart(organGraph, organGraphContext);

const userGraphContext = {
    type: 'doughnut',
    data: {
    labels: ['Hospitals', 'Donors', 'Patients'],
    datasets: [{
        label: 'My First Dataset',
        data: [hospitalCount, donorCount, patientCount],
        backgroundColor: [
            'rgb(54, 162, 235)',
            'rgb(255, 99, 132)',
            'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
    }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
    }
}

const drawUserGraph = new Chart(userGraph, userGraphContext);

userDetails.addEventListener('click', () => {
    location.href = "#user-details"
}); 