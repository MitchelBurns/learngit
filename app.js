let map;
let marker;
let lotsData = [];

// ─── Map Initialization ───────────────────────────────────────────────────────

function initMap() {
    const defaultCenter = { lat: 40.5119, lng: -111.3706 };
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: defaultCenter,
        mapTypeId: 'hybrid'
    });
}

// ─── Data Loading ─────────────────────────────────────────────────────────────

async function loadLotData() {
    try {
        const response = await fetch('lots.json');
        const data = await response.json();
        lotsData = data.lots;
    } catch (error) {
        showError('Error loading lot data. Please make sure lots.json is in the same folder.');
        console.error('Error:', error);
    }
}

// ─── Fuzzy / Partial Match Search ────────────────────────────────────────────

function partialMatch(value, searchTerm) {
    if (!value || !searchTerm) return false;
    return value.toString().toLowerCase().includes(searchTerm.toLowerCase().trim());
}

function searchLots() {
    const searchType  = document.getElementById('searchType').value;
    const searchInput = document.getElementById('searchInput').value.trim();

    hideError();
    hideDropdown();
    hideLotInfo();

    if (!searchInput) {
        showError('Please enter a search term');
        return;
    }

    let results = [];

    if (searchType === 'lotNumber') {
        results = lotsData.filter(l =>
            partialMatch(l.lotNumber, searchInput) || partialMatch(l.lotIdCRM, searchInput)
        );
    } else if (searchType === 'name') {
        results = lotsData.filter(l => partialMatch(l.ownerName, searchInput));
    } else if (searchType === 'address') {
        results = lotsData.filter(l => partialMatch(l.address, searchInput));
    }

    if (results.length === 0) {
        showError(`No lots found matching "${searchInput}"`);
    } else if (results.length === 1) {
        selectLot(results[0]);
    } else {
        showDropdown(results, searchType);
    }
}

// ─── Dropdown ─────────────────────────────────────────────────────────────────

function showDropdown(results, searchType) {
    const dropdown    = document.getElementById('searchDropdown');
    const resultsList = document.getElementById('resultsList');
    const countLabel  = document.getElementById('resultsCount');

    countLabel.textContent = `${results.length} match${results.length !== 1 ? 'es' : ''} found - select one:`;
    resultsList.innerHTML  = '';

    results.forEach(lot => {
        const li = document.createElement('li');
        li.className = 'result-item';

        let primary   = '';
        let secondary = '';

        if (searchType === 'name') {
            primary   = lot.ownerName || 'Unknown Owner';
            secondary = `Lot ${lot.lotNumber} &nbsp;·&nbsp; ${lot.address}`;
        } else {
            primary   = lot.address;
            secondary = `Lot ${lot.lotNumber} &nbsp;·&nbsp; Owner: ${lot.ownerName || 'N/A'}`;
        }

        li.innerHTML = `
            <span class="result-primary">${primary}</span>
            <span class="result-secondary">${secondary}</span>
        `;

        li.addEventListener('click', () => {
            selectLot(lot);
            hideDropdown();
        });

        resultsList.appendChild(li);
    });

    dropdown.classList.remove('hidden');
}

function hideDropdown() {
    document.getElementById('searchDropdown').classList.add('hidden');
}

// ─── Select a Lot ─────────────────────────────────────────────────────────────

function selectLot(lot) {
    showLotOnMap(lot);
    displayLotInfo(lot);
}

// ─── Map Pin ──────────────────────────────────────────────────────────────────

function showLotOnMap(lot) {
    const position = { lat: lot.coordinates.lat, lng: lot.coordinates.lng };

    if (marker) marker.setMap(null);

    marker = new google.maps.Marker({
        position,
        map,
        title: `Lot ${lot.lotNumber}`,
        animation: google.maps.Animation.DROP
    });

    map.setCenter(position);
    map.setZoom(18);

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="padding:10px;min-width:180px;">
                <strong style="font-size:15px;">Lot ${lot.lotNumber}</strong><br>
                <span style="font-size:13px;color:#555;">${lot.address}</span><br>
                <span style="margin-top:6px;display:inline-block;color:#555;">
                    Owner: ${lot.ownerName || 'N/A'}
                </span>
            </div>`
    });

    marker.addListener('click', () => infoWindow.open(map, marker));
}

// ─── Get Directions ───────────────────────────────────────────────────────────

function getDirections(lat, lng) {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
    window.open(url, '_blank');
}

// ─── Info Panel ───────────────────────────────────────────────────────────────

function displayLotInfo(lot) {
    const lotInfoDiv    = document.getElementById('lotInfo');
    const lotDetailsDiv = document.getElementById('lotDetails');

    const row = (label, value) => `
        <div class="detail-row">
            <span class="detail-label">${label}:</span>
            <span class="detail-value">${value || 'N/A'}</span>
        </div>`;

    // Directions button is FIRST, then all the detail rows
    lotDetailsDiv.innerHTML =
        `<div class="directions-row">
            <button class="btn-directions" onclick="getDirections(${lot.lat}, ${lot.lng})">
                🗺️ Get Directions
            </button>
        </div>` +
        row('Lot Number',           lot.lotNumber) +
        row('Lot ID (CRM)',         lot.lotIdCRM) +
        row('Address',              lot.address) +
        row('Acreage',              lot.acreage) +
        row('Has Water Assessment', lot.hasWaterAssessment) +
        row('Lot Type',             lot.lotType) +
        row('Phase Name',           lot.phaseName) +
        row('Membership Type',      lot.membershipType) +
        row('Membership Status',    lot.membershipStatus) +
        row('Jonas Member #',       lot.jonasMemberNumber) +
        row('Membership Period',    lot.membershipPeriod) +
        row('Owner Name',           lot.ownerName);

    lotInfoDiv.classList.remove('hidden');
}

function hideLotInfo() {
    document.getElementById('lotInfo').classList.add('hidden');
}

// ─── Error Helpers ────────────────────────────────────────────────────────────

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}

// ─── Clear / Reset ────────────────────────────────────────────────────────────

function clearSearch() {
    document.getElementById('searchInput').value = '';
    hideLotInfo();
    hideError();
    hideDropdown();

    if (marker) marker.setMap(null);

    map.setCenter({ lat: 40.5119, lng: -111.3706 });
    map.setZoom(15);
}

// ─── Event Listeners ──────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadLotData();

    document.getElementById('searchButton').addEventListener('click', searchLots);
    document.getElementById('clearButton').addEventListener('click', clearSearch);

    document.getElementById('searchInput').addEventListener('keypress', e => {
        if (e.key === 'Enter') searchLots();
    });

    document.getElementById('searchType').addEventListener('change', () => {
        const type = document.getElementById('searchType').value;
        const placeholders = {
            lotNumber: 'Enter lot number (e.g. 102)',
            name:      'Enter owner name (e.g. Smith)',
            address:   'Enter address (e.g. Haystack)'
        };
        document.getElementById('searchInput').placeholder = placeholders[type];
        hideDropdown();
        hideError();
    });

    document.addEventListener('click', e => {
        const dropdown = document.getElementById('searchDropdown');
        if (!dropdown.contains(e.target) &&
            e.target.id !== 'searchButton' &&
            e.target.id !== 'searchInput') {
            hideDropdown();
        }
    });
});