window.onload = function () {
    const success = document.getElementById("success-flag");
    if (success && success.value === "true") {
        alert("Product added successfully!");
    }
};

document.addEventListener("DOMContentLoaded", function () {
    if (window.alertMessages && window.alertMessages.length > 0) {
        window.alertMessages.forEach(msg => alert(msg));
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality
    const imageInput = document.getElementById('{{ form.image.id_for_label }}');
    const previewContainer = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    previewContainer.classList.remove('d-none');
                }
                reader.readAsDataURL(file);
            } else {
                previewContainer.classList.add('d-none');
            }
        });
    }
    
    // Success message using Bootstrap toast
    const successFlag = document.getElementById('success-flag');
    if (successFlag && successFlag.value === 'true') {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast
        const toastEl = document.createElement('div');
        toastEl.className = 'toast text-bg-success';
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        toastEl.innerHTML = `
            <div class="toast-header">
                <strong class="me-auto">Success</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                Product added successfully!
            </div>
        `;
        
        toastContainer.appendChild(toastEl);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
    
    // Initialize map if script is loaded
    if (typeof initMap === 'function') {
        initMap();
    }
    
    // Use current location button
    const useCurrentLocationBtn = document.getElementById('use-current-location');
    if (useCurrentLocationBtn) {
        useCurrentLocationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    // Update form fields
                    document.getElementById('{{ form.lat.id_for_label }}').value = lat;
                    document.getElementById('{{ form.lng.id_for_label }}').value = lng;
                    
                    // Update map if available
                    if (typeof updateMapMarker === 'function') {
                        updateMapMarker(lat, lng);
                    }
                });
            }
        });
    }
});

// my_bids

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show active tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabName + '-bids').classList.add('active');
        });
    });
    
    // Modal functionality
    const editModal = document.getElementById('edit-bid-modal');
    const removeModal = document.getElementById('remove-bid-modal');
    const closeButtons = document.querySelectorAll('.close-modal');
    
    // Edit bid functionality
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const bidId = this.getAttribute('data-bid-id');
            const price = this.getAttribute('data-price');
            const quantity = this.getAttribute('data-quantity');
            
            document.getElementById('edit-bid-id').value = bidId;
            document.getElementById('edit-price').value = price;
            document.getElementById('edit-quantity').value = quantity;
            
            editModal.style.display = 'block';
        });
    });
    
    // Remove bid functionality
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const bidId = this.getAttribute('data-bid-id');
            document.getElementById('remove-bid-id').value = bidId;
            removeModal.style.display = 'block';
        });
    });
    
    // Close modals
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            editModal.style.display = 'none';
            removeModal.style.display = 'none';
        });
    });
    
    // Close modals if clicked outside
    window.addEventListener('click', function(event) {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
        if (event.target === removeModal) {
            removeModal.style.display = 'none';
        }
    });
});

navigator.geolocation.getCurrentPosition(function(position) {
    document.getElementById("id_lat").value = position.coords.latitude;
    document.getElementById("id_lng").value = position.coords.longitude;
});