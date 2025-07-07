document.addEventListener("DOMContentLoaded", function () {
    // Fixed JS for property page interaction

    const map = L.map('propertyMap').setView([20.5937, 78.9629], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const properties = {};

    fetch('/search/?ajax=1', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(res => res.json())
        .then(data => {
            data.properties.forEach(p => {
                properties[p.id] = p;

                if (p.location && p.location.latitude && p.location.longitude) {
                    const lat = parseFloat(p.location.latitude);
                    const lng = parseFloat(p.location.longitude);
                    if (!isNaN(lat) && !isNaN(lng)) {
                        const marker = L.marker([lat, lng])
                            .addTo(map)
                            .bindPopup(`<b>${p.title}</b><br>${p.property_type}`)
                            .on('click', () => showPropertyDetails(p.id));
                        properties[p.id].marker = marker;
                    }
                }
            });

            initFeaturedProperties();
            initPropertyCards();

            const bounds = Object.values(properties)
                .filter(p => p.marker)
                .map(p => p.marker.getLatLng());
            if (bounds.length) map.fitBounds(L.latLngBounds(bounds));
        })
        .catch(err => {
            console.error("Property fetch failed", err);
            initPropertyCards();
        });

    const modal = document.getElementById('propertyModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalImage = document.getElementById('modalImage');
    const modalPrice = document.getElementById('modalPrice');
    const modalDetails = document.getElementById('modalDetails');
    const modalDescription = document.getElementById('modalDescription');
    const viewDetailsBtn = document.getElementById('viewDetailsBtn');
    const closeBtn = document.querySelector('.close');

    function showPropertyDetails(id) {
        const p = properties[id];
        if (!p) return showDefaultDetails();

        modalTitle.textContent = p.title;
        modalImage.src = p.main_image || defaultImageUrl;
        modalPrice.textContent = p.price_display || `$${p.price}`;
        modalDescription.textContent = p.description;
        viewDetailsBtn.href = p.detail_url;
        viewDetailsBtn.style.display = 'block';

        modalDetails.innerHTML = `
            <div><span>🏠</span> ${p.property_type}</div>
            <div><span>🛏</span> ${p.bedrooms} Bedrooms</div>
            <div><span>🛁</span> ${p.bathrooms} Bathrooms</div>
            <div><span>📏</span> ${p.square_feet} sqft</div>
            ${p.year_built ? `<div><span>🏗</span> Built ${p.year_built}</div>` : ''}
        `;
        showModal();
    }

    function showDefaultDetails() {
        modalTitle.textContent = "Property Details";
        modalImage.src = defaultImageUrl;
        modalPrice.textContent = "$---,---";
        modalDescription.textContent = "Details for this property are not available.";
        modalDetails.innerHTML = `
            <div><span>🏠</span> Unknown Property Type</div>
            <div><span>🛏</span> -- Bedrooms</div>
            <div><span>🛁</span> -- Bathrooms</div>
        `;
        viewDetailsBtn.style.display = 'none';
        showModal();
    }

    function showModal() {
        modal.style.display = 'block';
        setTimeout(() => modal.classList.add('show'), 10);
    }

    function hideModal() {
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 300);
    }

    closeBtn.addEventListener('click', hideModal);
    window.addEventListener('click', (e) => {
        if (e.target === modal) hideModal();
    });

    function initFeaturedProperties() {
        const featured = document.querySelectorAll('.featured-property');
        featured.forEach(el => {
            const id = el.getAttribute('data-id');
            const p = properties[id];
            if (!p) return;

            const img = el.querySelector('img');
            const title = el.querySelector('h3');
            const spans = el.querySelectorAll('.property-meta span');
            const price = el.querySelector('.property-price');

            if (img) img.src = p.main_image || defaultImageUrl;
            if (title) title.textContent = p.title;
            if (spans.length >= 3) {
                spans[0].textContent = `🏠 ${p.property_type}`;
                spans[1].textContent = `🛏 ${p.bedrooms} Beds`;
                spans[2].textContent = `🛁 ${p.bathrooms} Baths`;
            }
            if (price) price.textContent = p.price_display || `$${p.price}`;

            el.addEventListener('click', () => showPropertyDetails(id));
        });
    }

    function initPropertyCards() {
        const cards = document.querySelectorAll('.property-card');
        cards.forEach(card => {
            const id = card.getAttribute('data-id');
            const p = properties[id];
            const img = card.querySelector('img');
            const title = card.querySelector('p');

            if (p) {
                if (img) img.src = p.main_image || defaultImageUrl;
                if (title) title.textContent = p.title;
                card.addEventListener('click', () => showPropertyDetails(id));
            } else {
                card.addEventListener('click', showDefaultDetails);
            }
        });
    }
});
