// Main JavaScript file for RansomSim

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if needed
    initializeTooltips();
    
    // Initialize countdown timers
    initializeCountdownTimers();
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

function initializeTooltips() {
    // Bootstrap 5 tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility function to show notifications
function showNotification(message, type = 'info', duration = 3000) {
    const alertClass = `alert-${type}`;
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main .container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, duration);
    }
}

// Utility function to confirm action
function confirmAction(message = 'Are you sure?') {
    return confirm(message);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success', 2000);
    }).catch(() => {
        showNotification('Failed to copy', 'danger', 2000);
    });
}

// Initialize countdown timers
function initializeCountdownTimers() {
    const countdownElements = document.querySelectorAll('.countdown');
    countdownElements.forEach(element => {
        updateCountdown(element);
        // Update every second
        setInterval(() => updateCountdown(element), 1000);
    });
}

// Update a single countdown timer
function updateCountdown(element) {
    const deadlineStr = element.getAttribute('data-deadline');
    if (!deadlineStr) return;
    
    // Parse the datetime string (format: YYYY-MM-DDTHH:MM or YYYY-MM-DD HH:MM:SS)
    const deadlineDate = new Date(deadlineStr.replace(' ', 'T'));
    const now = new Date();
    const diff = deadlineDate - now;
    
    if (diff <= 0) {
        element.innerHTML = '<span style="color: #dc3545; font-weight: bold;">⏰ EXPIRED</span>';
        return;
    }
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    let timeStr = '';
    if (days > 0) timeStr += `${days}d `;
    if (hours > 0 || days > 0) timeStr += `${hours}h `;
    if (minutes > 0 || hours > 0 || days > 0) timeStr += `${minutes}m `;
    timeStr += `${seconds}s`;
    
    // Change color based on remaining time
    let color = '#28a745'; // Green
    if (diff < 24 * 60 * 60 * 1000) color = '#ffc107'; // Yellow - less than 1 day
    if (diff < 6 * 60 * 60 * 1000) color = '#dc3545'; // Red - less than 6 hours
    
    element.innerHTML = `<span style="color: ${color}; font-weight: bold;">⏱️ ${timeStr}</span>`;
}
