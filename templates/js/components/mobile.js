export function setupMobileHandlers(coordContainer, map) {
    const mobileToggle = document.querySelector('.mobile-toggle');
    
    if (!mobileToggle) return;

    mobileToggle.addEventListener('click', () => {
        coordContainer.classList.toggle('show-mobile');
        setTimeout(() => {
            map.invalidateSize();
        }, 300);
    });

    // Cerrar panel al hacer click en el mapa en móvil
    if (window.innerWidth <= 768) {
        map.on('click', () => {
            coordContainer.classList.remove('show-mobile');
            setTimeout(() => {
                map.invalidateSize();
            }, 300);
        });
    }
} 