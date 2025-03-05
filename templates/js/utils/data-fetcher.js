import { showNotification } from '../components/notifications.js';
import { updateMarker } from '../components/map.js';
import { updateInfoPanel } from '../components/sidebar.js';

export async function fetchLocations(map, markers) {
    try {
        const response = await fetch('/get_all_locations');
        if (!response.ok) throw new Error('Error en la respuesta del servidor');

        const locations = await response.json();
        if (!locations) throw new Error('No hay datos de ubicación');

        Object.entries(locations).forEach(([deviceId, locationData]) => {
            if (locationData?.latitude && locationData?.longitude) {
                updateMarker(deviceId, locationData, markers, map);
                updateInfoPanel(deviceId, locationData);
            }
        });
    } catch (error) {
        console.error('Error fetching locations:', error);
        showNotification('Error al actualizar ubicaciones', 'error');
    }
} 