export const MAP_CONFIG = {
    defaultCenter: [10.4806, -66.9036], // Caracas
    defaultZoom: 15,
    satelliteUrl: 'http://mt{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    streetsUrl: 'http://mt{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attribution: '© Google',
    subdomains: '0123'
};

export const ANTENNAS_CONFIG = {
    'OFICINA EMBARCACIONES': {
        id: 'oficina',
        name: 'OFICINA EMBARCACIONES',
        shortName: 'OE',
        timeoutThreshold: 120000,
        icon: 'fa-satellite-dish'
    },
    'RM MERIDA': {
        id: 'merida',
        name: 'RM MÉRIDA',
        shortName: 'RM',
        timeoutThreshold: Infinity,
        icon: 'fa-satellite-dish',
        forceActive: true
    },
    'Rio Caribe': {
        id: 'riocaribe',
        name: 'RM RIO CARIBE',
        shortName: 'RC',
        timeoutThreshold: 120000,
        icon: 'fa-satellite-dish'
    }
}; 