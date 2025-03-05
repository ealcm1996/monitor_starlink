import { isDeviceActive } from '../utils/device-status.js';

export function createPopupContent(deviceId, locationData, isActive) {
    const forceActive = deviceId === 'RM MERIDA';
    const deviceActive = forceActive || isActive;

    const antennaNames = {
        'OFICINA EMBARCACIONES': 'OFICINA EMBARCACIONES',
        'Rio Caribe': 'RM RIO CARIBE',
        'RM MERIDA': 'RM MÉRIDA'
    };

    return `
        <div class="custom-popup">
            <!-- ... contenido del popup ... -->
        </div>
    `;
} 