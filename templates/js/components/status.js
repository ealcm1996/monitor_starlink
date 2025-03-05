import { ANTENNAS_CONFIG } from '../config/config.js';

export function updateDeviceStatus(deviceId, timestamp) {
    const config = ANTENNAS_CONFIG[deviceId];
    if (!config) return false;

    if (config.forceActive) return true;

    const timeDiff = Date.now() - timestamp;
    return timeDiff < config.timeoutThreshold;
}

export function formatTimeDiff(timestamp) {
    const diff = Date.now() - timestamp;
    const seconds = Math.floor(diff / 1000);
    
    if (seconds < 60) {
        return `Hace ${seconds} segundos`;
    }
    
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) {
        return `Hace ${minutes} minutos`;
    }
    
    const hours = Math.floor(minutes / 60);
    return `Hace ${hours} horas`;
} 