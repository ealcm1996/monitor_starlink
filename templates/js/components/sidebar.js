import { isDeviceActive } from '../utils/device-status.js';

export function updateInfoPanel(deviceId, locationData) {
    const idMapping = {
        'OFICINA EMBARCACIONES': 'oficina',
        'RM MERIDA': 'merida',
        'Rio Caribe': 'riocaribe'
    };

    const panelId = idMapping[deviceId];
    if (!panelId) return;

    const infoBox = document.querySelector(`#coordinates-${panelId}`);
    if (!infoBox) return;

    const deviceActive = isDeviceActive(deviceId, locationData);

    // Actualizar clases y estados
    infoBox.classList.toggle('active', deviceActive);
    
    const infoElement = infoBox.querySelector('.coordinates-info');
    if (infoElement) {
        infoElement.innerHTML = `
            <p>
                <span>Estado:</span> 
                <span class="${deviceActive ? 'active' : 'inactive'}">
                    ${deviceActive ? 'En línea' : 'Desconectado'}
                </span>
            </p>
            <p><span>Latitud:</span> <span>${locationData.latitude.toFixed(6)}°</span></p>
            <p><span>Longitud:</span> <span>${locationData.longitude.toFixed(6)}°</span></p>
            <p><span>Altitud:</span> <span>${locationData.altitude?.toFixed(1) || 0}m</span></p>
            <p><span>Actualización:</span> <span>${new Date(locationData.timestamp).toLocaleString()}</span></p>
        `;
    }
} 