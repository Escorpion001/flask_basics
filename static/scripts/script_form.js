// Form validation: check if passwords match
function validateForm() {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm_password').value;

  if (password !== confirmPassword) {
      alert('Passwords do not match. Please try again.');
      return false;
  }

  return true; // Submit form if everything is valid
}
