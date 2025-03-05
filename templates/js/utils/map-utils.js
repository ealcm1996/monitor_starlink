export function initMap(config) {
    const map = L.map('map', {
        center: config.defaultCenter,
        zoom: config.defaultZoom,
        zoomControl: true,
        attributionControl: true
    });

    // Añadir capas de mapa
    const satellite = L.tileLayer(config.satelliteUrl, {
        maxZoom: 19,
        attribution: config.attribution
    }).addTo(map);

    const streets = L.tileLayer(config.streetsUrl, {
        maxZoom: 19,
        attribution: config.attribution
    });

    // Añadir control de capas
    const baseMaps = {
        "Satélite": satellite,
        "Calles": streets
    };

    L.control.layers(baseMaps).addTo(map);

    return map;
} 