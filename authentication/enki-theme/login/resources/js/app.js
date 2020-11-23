document.addEventListener("DOMContentLoaded", function() {
  var loginInputs = document.querySelectorAll('.js-loginInputs');
  var usernameInput = document.querySelector('#username');
  var passwordInput = document.querySelector('#password');
  var loginSubmit = document.querySelector('#kc-login');
  var showPwd = document.querySelector('.js-showPwd');
  Array.prototype.forEach.call(loginInputs, function(loginInput) {
    if (!loginInput) return;
    loginInput.addEventListener('keyup', function() {
      if (usernameInput.value !== '' && passwordInput.value !== '') {
        loginSubmit.disabled = false;
      } else {
        loginSubmit.disabled = true;
      }
    })
  })
  if (showPwd) {
    showPwd.addEventListener('click', function() {
      if (passwordInput.type === "password") {
        passwordInput.type = "text"
        showPwd.classList.add('-active')
      } else {
        passwordInput.type = "password"
        showPwd.classList.remove('-active')
      }
    })
  }

});