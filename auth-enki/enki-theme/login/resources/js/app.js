document.addEventListener("DOMContentLoaded", function() {
  var loginInputs = document.querySelectorAll('.js-loginInputs');
  var usernameInput = document.querySelector('#username');
  var passwordInput = document.querySelector('#password');
  var loginSubmit = document.querySelector('#kc-login');
  Array.prototype.forEach.call(loginInputs, function(loginInput) {
    loginInput.addEventListener('keyup', function(){
      if (usernameInput.value !== '' && passwordInput.value !== '') {
        loginSubmit.disabled = false;
      } else {
        loginSubmit.disabled = true;
      }
    })
  })
});