document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Handle alert messages
    if (window.alertMessages && window.alertMessages.length) {
        const alertsContainer = document.createElement('div');
        alertsContainer.className = 'alerts-container position-fixed top-0 end-0 p-3';
        alertsContainer.style.zIndex = '1050';
        
        window.alertMessages.forEach(message => {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'toast';
            alertDiv.setAttribute('role', 'alert');
            alertDiv.setAttribute('aria-live', 'assertive');
            alertDiv.setAttribute('aria-atomic', 'true');
            
            // Detect message type
            let alertClass = 'bg-info text-white';
            if (message.toLowerCase().includes('success')) {
                alertClass = 'bg-success text-white';
            } else if (message.toLowerCase().includes('error') || message.toLowerCase().includes('failed')) {
                alertClass = 'bg-danger text-white';
            }
            
            alertDiv.innerHTML = `
                <div class="toast-header ${alertClass}">
                    <strong class="me-auto">Notification</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            `;
            
            alertsContainer.appendChild(alertDiv);
            
            // Initialize and show the toast
            const toast = new bootstrap.Toast(alertDiv, {
                autohide: true,
                delay: 5000
            });
            toast.show();
        });
        
        document.body.appendChild(alertsContainer);
    }
});

// document.getElementById('predictPriceForm').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent default form submission

//     // Collect form data
//     var formData = new FormData(this);

//     // Send AJAX request to predict the price
//     fetch("{% url 'predict_price' %}", {
//         method: "POST",
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Handle the response - update the page with the predicted price
//         if (data.predicted_price) {
//             const alertDiv = document.querySelector('.alert-info');
//             alertDiv.innerHTML = `<strong>Predicted Price:</strong> ₹${data.predicted_price}`;
//             alertDiv.style.display = 'block'; // Make sure the alert is visible
//         } else if (data.error) {
//             alert("Error: " + data.error);
//         }
//     })
//     .catch(error => {
//         console.error("Error:", error);
//         alert("An error occurred while predicting the price.");
//     });
// });

document.getElementById('predictPriceModal').addEventListener('submit', function() {
    const btn = document.getElementById('predictSubmitBtn');
    btn.disabled = true;
    btn.querySelector('.spinner-border').classList.remove('d-none');
});