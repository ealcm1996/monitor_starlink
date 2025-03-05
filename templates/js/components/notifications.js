export function showNotification(message, type = 'success') {
    const notification = document.getElementById(`${type}Notification`);
    if (!notification) return;

    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
} 