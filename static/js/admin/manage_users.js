document.addEventListener('DOMContentLoaded', function() {
    // Setup delete user modal
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteUserModal'));
    const deleteUserName = document.getElementById('deleteUserName');
    const deleteUserForm = document.getElementById('deleteUserForm');
    
    // Add event listeners to all delete buttons
    document.querySelectorAll('.delete-user-btn').forEach(button => {
        button.addEventListener('click', function() {
            const username = this.getAttribute('data-username');
            const userId = this.getAttribute('data-user-id');
            const userType = this.getAttribute('data-user-type');
            
            // Set the modal content
            deleteUserName.textContent = username;
            deleteUserForm.action = "{% url 'delete_user' 0 %}".replace('0', userId);
            
            // Show the modal
            deleteModal.show();
        });
    });
    
    // Show toast notification if there's a message in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    
    if (message) {
        const toastContainer = document.querySelector('.toast-container');
        const toastEl = document.createElement('div');
        toastEl.className = 'toast';
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        // Check message type
        let toastClass = 'bg-info text-white';
        let icon = 'info-circle-fill';
        if (message.toLowerCase().includes('success') || message.toLowerCase().includes('deleted')) {
            toastClass = 'bg-success text-white';
            icon = 'check-circle-fill';
        } else if (message.toLowerCase().includes('error') || message.toLowerCase().includes('failed')) {
            toastClass = 'bg-danger text-white';
            icon = 'exclamation-circle-fill';
        }
        
        toastEl.innerHTML = `
            <div class="toast-header ${toastClass}">
                <i class="bi bi-${icon} me-2"></i>
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        toastContainer.appendChild(toastEl);
        
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
        toast.show();
        
        // Remove message parameter from URL without reloading the page
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});