document.addEventListener('DOMContentLoaded', function() {
  // Get all menu items and panels
  const menuItems = document.querySelectorAll('.menu-item');
  const panels = document.querySelectorAll('.content-panel');
  
  // Handle menu item clicks
  menuItems.forEach(item => {
      item.addEventListener('click', function() {
          // Remove active class from all menu items
          menuItems.forEach(i => i.classList.remove('active'));
          
          // Add active class to clicked menu item
          this.classList.add('active');
          
          // Get the panel to show
          const panelId = this.getAttribute('data-panel') + '-panel';
          
          // Hide all panels
          panels.forEach(panel => panel.classList.remove('active'));
          
          // Show the selected panel
          document.getElementById(panelId).classList.add('active');
          
          // Special case for logout - we might want to handle differently
          if (panelId === 'logout-panel') {
              // Could add specific logout logic here
          }
      });
  });
  
  // Patient form toggle
  const addPatientBtn = document.getElementById('addPatientBtn');
  const patientFormSection = document.getElementById('patientFormSection');
  const cancelPatientForm = document.getElementById('cancelPatientForm');
  
  if (addPatientBtn && patientFormSection && cancelPatientForm) {
      addPatientBtn.addEventListener('click', function() {
          patientFormSection.style.display = 'block';
          // Scroll to the form
          patientFormSection.scrollIntoView({ behavior: 'smooth' });
      });
      
      cancelPatientForm.addEventListener('click', function() {
          patientFormSection.style.display = 'none';
      });
  }
  
  // Form submission
  const patientForm = document.getElementById('patientForm');
  if (patientForm) {
      patientForm.addEventListener('submit', function(e) {
          e.preventDefault();
          alert('Patient registration submitted successfully!');
          patientForm.reset();
          patientFormSection.style.display = 'none';
      });
  }
  
  // Settings form submission
  const settingsForm = document.getElementById('settingsForm');
  if (settingsForm) {
      settingsForm.addEventListener('submit', function(e) {
          e.preventDefault();
          alert('Settings saved successfully!');
      });
  }
  
  // Generate sample data (for demonstration)
  function generateSampleData() {
      // In a real app, this would come from an API
      console.log('Sample data loaded');
  }
  
  generateSampleData();
});

// Utility functions
function generatePatientID() {
  const prefix = 'PAT';
  const randomNum = Math.floor(10000 + Math.random() * 90000);
  return `${prefix}${randomNum}`;
}

function getCurrentDate() {
  const today = new Date();
  return today.toISOString().split('T')[0];
}