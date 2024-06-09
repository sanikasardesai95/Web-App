document.getElementById('contactForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
      name: document.getElementById('name').value,
      email: document.getElementById('email').value,
      phone: document.getElementById('phone').value,
      message: document.getElementById('message').value
    };
    
    try {
      const response = await fetch('/api/form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
  
      const result = await response.json();
  
      document.getElementById('response').innerText = result.message;
      document.getElementById('contactForm').reset();
    } catch (error) {
      document.getElementById('response').innerText = 'There was an error submitting the form.';
      console.error('Error:', error);
    }
  });
  