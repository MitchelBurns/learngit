// JavaScript source code
let map;
let marker;
let lotsData = [];

/*const lotsData = [
    {
        "lotNumber": "101",
        "address": "123 Main Street",
        "coordinates": { "lat": 40.7128, "lng": -74.0060 },
        "size": "0.25 acres",
        "status": "Available",
        "price": "$45,000",
        "features": ["Corner lot", "Utilities available"]
    }
    // Add more lots here
];*/

// Initialize the map
function initMap() {
    // Default center (you can change this to your community's center)
    const defaultCenter = { lat: 40.7128, lng: -74.0060 };

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: defaultCenter,
        mapTypeId: 'hybrid'
    });
}

// Load lot data from JSON file
async function loadLotData() {
    try {
        const response = await fetch('lots_geocoded.json');
        const data = await response.json();
        lotsData = data.lots;
    } catch (error) {
        showError('Error loading lot data. Please make sure lots.json is in the same folder.');
        console.error('Error:', error);
    }
}

// Search for a lot
function searchLot() {
    const lotNumber = document.getElementById('lotNumberInput').value.trim();

    if (!lotNumber) {
        showError('Please enter a lot number');
        return;
    }

    const lot = lotsData.find(l => l.lotNumber === lotNumber);

    if (lot) {
        hideError();
        showLotOnMap(lot);
        displayLotInfo(lot);
    } else {
        showError(`Lot number "${lotNumber}" not found. Please check the lot number and try again.`);
        hideLotInfo();
    }
}

// Show lot on map with marker
function showLotOnMap(lot) {
    const position = { lat: lot.coordinates.lat, lng: lot.coordinates.lng };

    // Remove existing marker if any
    if (marker) {
        marker.setMap(null);
    }

    // Create new marker
    marker = new google.maps.Marker({
        position: position,
        map: map,
        title: `Lot ${lot.lotNumber}`,
        animation: google.maps.Animation.DROP
    });

    // Center map on the lot
    map.setCenter(position);
    map.setZoom(18);

    // Create info window
    const infoWindow = new google.maps.InfoWindow({
        content: `<div style="padding: 10px;">
                    <h3>Lot ${lot.lotNumber}</h3>
                    <p>${lot.address}</p>
                    <p><strong>${lot.status}</strong></p>
                  </div>`
    });

    // Show info window on marker click
    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });
}

// Display lot information in the sidebar
function displayLotInfo(lot) {
    const lotInfoDiv = document.getElementById('lotInfo');
    const lotDetailsDiv = document.getElementById('lotDetails');

    const statusClass = lot.status.toLowerCase() === 'available' ? 'status-available' : 'status-sold';

    const featuresHTML = lot.features.map(feature => `<li>${feature}</li>`).join('');

    lotDetailsDiv.innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Lot Number:</span>
            <span class="detail-value">${lot.lotNumber}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Address:</span>
            <span class="detail-value">${lot.address}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Size:</span>
            <span class="detail-value">${lot.size}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Status:</span>
            <span class="detail-value ${statusClass}">${lot.status}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Price:</span>
            <span class="detail-value">${lot.price}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Features:</span>
            <ul class="features-list">
                ${featuresHTML}
            </ul>
        </div>
    `;

    lotInfoDiv.classList.remove('hidden');
}

// Hide lot information
function hideLotInfo() {
    document.getElementById('lotInfo').classList.add('hidden');
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

// Hide error message
function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}

// Clear search
function clearSearch() {
    document.getElementById('lotNumberInput').value = '';
    hideLotInfo();
    hideError();

    if (marker) {
        marker.setMap(null);
    }

    // Reset map to default view
    map.setCenter({ lat: 40.7128, lng: -74.0060 });
    map.setZoom(15);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadLotData();

    document.getElementById('searchButton').addEventListener('click', searchLot);
    document.getElementById('clearButton').addEventListener('click', clearSearch);

    // Allow Enter key to search
    document.getElementById('lotNumberInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchLot();
        }
    });
});