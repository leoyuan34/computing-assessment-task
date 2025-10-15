var map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.marker([48.8566, 2.3522]).addTo(map).bindPopup("Paris, France");
L.marker([-33.8688, 151.2093]).addTo(map).bindPopup("Sydney, Australia");
