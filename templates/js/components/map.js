import { createPopupContent } from './popup.js';
import { isDeviceActive } from '../utils/device-status.js';

export function createCustomMarker(isActive) {
    return L.divIcon({
        className: 'custom-marker-container',
        html: `
            <div class="vessel-marker ${isActive ? 'active' : 'inactive'}">
                <div class="signal-ring"></div>
                <div class="vessel-icon"></div>
            </div>
        `,
        iconSize: [80, 80],
        iconAnchor: [40, 40]
    });
}

export function updateMarker(deviceId, locationData, markers, map) {
    const isActive = isDeviceActive(deviceId, locationData);

    if (!markers[deviceId]) {
        markers[deviceId] = L.marker([locationData.latitude, locationData.longitude], {
            icon: createCustomMarker(isActive)
        }).addTo(map);
    } else {
        markers[deviceId].setLatLng([locationData.latitude, locationData.longitude]);
        markers[deviceId].setIcon(createCustomMarker(isActive));
    }

    const popupContent = createPopupContent(deviceId, locationData, isActive);
    markers[deviceId].bindPopup(popupContent);
} 