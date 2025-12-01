/* eslint-disable */
// Favorites functionality
let favorites = JSON.parse(localStorage.getItem('propertyFavorites')) || [];

function toggleFavorite(propertyId) {
    const index = favorites.indexOf(propertyId);
    const favoriteBtn = document.querySelector(`[data-property-id="${propertyId}"] .property-favorite`);

    if (index > -1) {
        favorites.splice(index, 1);
        favoriteBtn.classList.remove('favorited');
    } else {
        favorites.push(propertyId);
        favoriteBtn.classList.add('favorited');
    }

    localStorage.setItem('propertyFavorites', JSON.stringify(favorites));
}

// Initialize favorites on page load
document.addEventListener('DOMContentLoaded', function() {
    favorites.forEach(propertyId => {
        const favoriteBtn = document.querySelector(`[data-property-id="${propertyId}"] .property-favorite`);
        if (favoriteBtn) {
            favoriteBtn.classList.add('favorited');
        }
    });
});

// View toggle functionality
function setView(viewType, buttonElement) {
    const gridView = document.getElementById('propertiesGrid');
    const listView = document.getElementById('propertiesList');
    const toggleButtons = document.querySelectorAll('.view-toggle button');

    toggleButtons.forEach(btn => btn.classList.remove('active'));
    buttonElement.classList.add('active');

    if (viewType === 'grid') {
        gridView.style.display = 'grid';
        listView.style.display = 'none';
    } else {
        gridView.style.display = 'none';
        listView.style.display = 'block';
    }
}



// Filter functionality
function applyFilters() {
    const propertyType = document.getElementById('propertyType').value;
    const location = document.getElementById('location').value;
    const priceRange = document.getElementById('priceRange').value;

    const propertyCards = document.querySelectorAll('.property-card');

    propertyCards.forEach(card => {
        let show = true;

        // Property type filter
        if (propertyType && !card.querySelector('.property-title').textContent.toLowerCase().includes(propertyType.toLowerCase())) {
            show = false;
        }

        // Location filter
        if (location && !card.querySelector('.property-location').textContent.includes(location)) {
            show = false;
        }

        // Price range filter (simplified - would need actual price data)
        if (priceRange) {
            // This would need to be implemented based on actual property data
            // For now, just show all
        }

        card.style.display = show ? 'block' : 'none';
    });
}

// Sort functionality
function sortProperties() {
    const sortBy = document.getElementById('sortBy').value;
    const grid = document.getElementById('propertiesGrid');
    const cards = Array.from(grid.children);

    cards.sort((a, b) => {
        switch (sortBy) {
            case 'price-low':
                return getPrice(a) - getPrice(b);
            case 'price-high':
                return getPrice(b) - getPrice(a);
            case 'newest':
                return 0; // Would need date data
            case 'oldest':
                return 0; // Would need date data
            case 'area':
                return getArea(b) - getArea(a);
            default:
                return 0;
        }
    });

    cards.forEach(card => grid.appendChild(card));
}

function getPrice(card) {
    const priceText = card.querySelector('.property-price').textContent;
    const match = priceText.match(/[\d,]+/);
    return match ? parseInt(match[0].replace(/,/g, '')) : 0;
}

function getArea(card) {
    const areaText = card.querySelector('.property-feature:last-child').textContent;
    const match = areaText.match(/(\d+)/);
    return match ? parseInt(match[1]) : 0;
}

// Clear filters
function clearFilters() {
    document.getElementById('propertyType').value = '';
    document.getElementById('location').value = '';
    document.getElementById('priceRange').value = '';

    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => card.style.display = 'block');
}

// Loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}
