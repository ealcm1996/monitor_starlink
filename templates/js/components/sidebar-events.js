import { ANTENNAS_CONFIG } from '../config/config.js';

export function setupSidebarEvents(map, markers) {
    const coordContainer = document.querySelector('.coordinates-container');
    const collapseButton = document.querySelector('.collapse-button');

    // Evento de colapsar
    collapseButton?.addEventListener('click', () => {
        coordContainer.classList.toggle('collapsed');
        collapseButton.querySelector('i').classList.toggle('fa-chevron-right');
        collapseButton.querySelector('i').classList.toggle('fa-chevron-left');
        setTimeout(() => map.invalidateSize(), 300);
    });

    // Eventos para cada antena
    Object.entries(ANTENNAS_CONFIG).forEach(([deviceId, config]) => {
        const box = document.querySelector(`#coordinates-${config.id}`);
        if (!box) return;

        box.addEventListener('click', () => {
            const marker = markers[deviceId];
            if (marker) {
                map.setView(marker.getLatLng(), 16, {
                    animate: true,
                    duration: 1
                });
                marker.openPopup();
            }
        });

        // Efectos hover
        box.addEventListener('mouseenter', () => {
            const marker = markers[deviceId];
            if (marker) {
                const element = marker.getElement();
                if (element) {
                    element.style.zIndex = 1000;
                    element.style.transform += ' scale(1.1)';
                }
            }
        });

        box.addEventListener('mouseleave', () => {
            const marker = markers[deviceId];
            if (marker) {
                const element = marker.getElement();
                if (element) {
                    element.style.zIndex = '';
                    element.style.transform = element.style.transform.replace(' scale(1.1)', '');
                }
            }
        });
    });
} 