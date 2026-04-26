function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function notification(text, type = 'info', time = 5000) {
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    const notif = document.createElement('div');
    notif.className = `notification ${type}`;
    notif.innerHTML = `
        <button class="notification-close">&times;</button>
        <span class="notification-text">${text}</span>
        <div class="notification-progress"></div>
    `;

    const progressBar = notif.querySelector('.notification-progress');
    progressBar.style.animationDuration = `${time}ms`;
    document.body.appendChild(notif);

    const closeBtn = notif.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        removeNotification(notif);
    });
    

    if (time > 0) {
        setTimeout(() => {
            removeNotification(notif);
        }, time);
    }
    
    function removeNotification(element) {
        // const progress = element.querySelector('.notification-progress');
        // const remaining = getComputedStyle(progress).width;
        
        // const totalWidth = element.offsetWidth;
        // const currentWidth = parseFloat(remaining);
        // const remainingTime = (currentWidth / totalWidth) * time;
        
        // progress.style.animation = 'none';
        // progress.style.width = currentWidth + 'px';

        element.style.animation = 'slideUp 0.3s ease forwards';
        setTimeout(() => {
            element.remove();
        }, 300);
    }
}

function printtt(text) {
    console.log(text);
}