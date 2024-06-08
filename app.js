// JavaScript form validation and submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent default form submission
        
        // Get form data
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const message = document.getElementById('message').value;
        
        // Basic validation
        if (name && email && phone && message) {
            // Form data object
            const formData = {
                name: name,
                email: email,
                phone: phone,
                message: message
            };
            
            // Simulate form submission (for demonstration purposes)
            console.log('Form submitted successfully!', formData);
            alert('Form submitted successfully!');

            // Optionally, clear the form
            form.reset();
        } else {
            alert('Please fill in all fields.');
        }
    });
});
