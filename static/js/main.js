// Main JavaScript for Praise & Worship Scheduler

// Dark Mode Toggle Functionality
(function() {
    // Get theme from localStorage or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    const html = document.documentElement;
    
    // Apply saved theme immediately (before DOMContentLoaded to prevent flash)
    html.setAttribute('data-theme', currentTheme);
    
    // Update icon based on theme
    function updateDarkModeIcon(theme) {
        const icon = document.getElementById('darkModeIcon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }
    
    // Toggle dark mode
    function toggleDarkMode() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateDarkModeIcon(newTheme);
    }
    
    // Initialize icon on page load
    document.addEventListener('DOMContentLoaded', function() {
        const toggleButton = document.getElementById('darkModeToggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', toggleDarkMode);
            updateDarkModeIcon(currentTheme);
        }
    });
})();

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds (except those with data-persist attribute)
    const alerts = document.querySelectorAll('.alert:not([data-persist])');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Custom Modern Modal Functions
function showCustomModal(title, content, icon = 'ℹ️', showCancel = false, onConfirm = null) {
    const modal = new bootstrap.Modal(document.getElementById('customModal'));
    const modalTitle = document.getElementById('modalTitle');
    const modalIcon = document.getElementById('modalIcon');
    const modalContent = document.getElementById('modalContent');
    const modalOkBtn = document.getElementById('modalOkBtn');
    const modalCancelBtn = document.getElementById('modalCancelBtn');
    
    // Set title and icon
    modalTitle.textContent = title;
    modalIcon.textContent = icon;
    
    // Set content - if it's already HTML, use it directly; otherwise format it
    if (typeof content === 'string') {
        // Check if content contains HTML tags
        if (content.includes('<') && content.includes('>')) {
            // It's already HTML, use it directly
            modalContent.innerHTML = content;
        } else {
            // It's plain text, format it with line breaks
            modalContent.innerHTML = content.split('\n').map(line => {
                if (line.trim() === '') return '<br>';
                // Format key-value pairs
                if (line.includes(':')) {
                    const [key, value] = line.split(':').map(s => s.trim());
                    return `<div class="mb-2"><strong style="color: #6b7d4a;">${key}:</strong> <span style="color: #1a2e1a;">${value}</span></div>`;
                }
                return `<div class="mb-2">${line}</div>`;
            }).join('');
        }
    } else {
        modalContent.innerHTML = content;
    }
    
    // Show/hide cancel button
    if (showCancel) {
        modalCancelBtn.style.display = 'inline-block';
    } else {
        modalCancelBtn.style.display = 'none';
    }
    
    // Set up OK button
    modalOkBtn.onclick = function() {
        modal.hide();
        if (onConfirm) {
            onConfirm();
        }
    };
    
    // Set up Cancel button
    modalCancelBtn.onclick = function() {
        modal.hide();
    };
    
    modal.show();
}

// Replace default alert with custom modal
function customAlert(message, title = 'Information', icon = 'ℹ️') {
    showCustomModal(title, message, icon, false);
}

// Replace default confirm with custom modal
function customConfirm(message, title = 'Confirm', icon = '❓', onConfirm = null, onCancel = null) {
    showCustomModal(title, message, icon, true, function() {
        if (onConfirm) onConfirm();
    });
    
    const modalCancelBtn = document.getElementById('modalCancelBtn');
    modalCancelBtn.onclick = function() {
        bootstrap.Modal.getInstance(document.getElementById('customModal')).hide();
        if (onCancel) onCancel();
    };
}

