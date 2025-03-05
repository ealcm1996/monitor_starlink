import { MAP_CONFIG } from './config/config.js';
import { initMap } from './utils/map-utils.js';
import { setupMobileHandlers } from './components/mobile.js';
import { fetchLocations } from './utils/data-fetcher.js';

// Estado global
const markers = {};
let map;

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar mapa
    map = initMap(MAP_CONFIG);
    
    // Configurar handlers móviles
    const coordContainer = document.querySelector('.coordinates-container');
    setupMobileHandlers(coordContainer, map);
    
    // Iniciar actualizaciones
    fetchLocations(map, markers);
    setInterval(() => fetchLocations(map, markers), 1000);
}); 