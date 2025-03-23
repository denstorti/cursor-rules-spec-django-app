/**
 * Main JavaScript for the Freelancer Marketplace application
 */

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Form field enhancement
    enhanceFormFields();
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

/**
 * Enhance form fields with appropriate classes and attributes
 */
function enhanceFormFields() {
    // Add Bootstrap classes to form elements that Django doesn't automatically add
    const textInputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="url"], input[type="number"]');
    textInputs.forEach(input => {
        input.classList.add('form-control');
    });
    
    const selects = document.querySelectorAll('select:not([multiple])');
    selects.forEach(select => {
        select.classList.add('form-select');
    });
    
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.classList.add('form-control');
    });
    
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.classList.add('form-check-input');
    });
} 