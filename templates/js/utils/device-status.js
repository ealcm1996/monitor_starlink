export function isDeviceActive(deviceId, locationData) {
    if (deviceId === 'RM MERIDA') {
        return true;
    }

    const timestamp = Number(locationData.timestamp);
    const timeDiff = Date.now() - timestamp;
    return timeDiff < 120000;
} 