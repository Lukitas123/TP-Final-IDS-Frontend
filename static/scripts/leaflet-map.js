document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([-41.134258, -71.308525], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([-41.134258, -71.308525]).addTo(map)
        .bindPopup('Hotel Bugbusters<br> Av. Bustillo Km 1.151, San Carlos de Bariloche')
        .openPopup();
});
