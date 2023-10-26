(function () {
  //Login/Signup modal window
  function ModalSignin(element) {
    this.element = element;
    this.blocks = this.element.getElementsByClassName("js-signin-modal-block");
    this.switchers = this.element
      .getElementsByClassName("js-signin-modal-switcher")[0]
      .getElementsByTagName("a");
    this.triggers = document.getElementsByClassName("js-signin-modal-trigger");
    this.hidePassword = this.element.getElementsByClassName("js-hide-password");
    this.init();
  }

  ModalSignin.prototype.init = function () {
    var self = this;
    //open modal/switch form
    for (var i = 0; i < this.triggers.length; i++) {
      (function (i) {
        self.triggers[i].addEventListener("click", function (event) {
          if (event.target.hasAttribute("data-signin")) {
            event.preventDefault();
            self.showSigninForm(event.target.getAttribute("data-signin"));
          }
        });
      })(i);
    }

    //hide/show password
    for (var i = 0; i < this.hidePassword.length; i++) {
      (function (i) {
        self.hidePassword[i].addEventListener("click", function (event) {
          self.togglePassword(self.hidePassword[i]);
        });
      })(i);
    }
  };

  ModalSignin.prototype.togglePassword = function (target) {
    var password = target.previousElementSibling;
    if ("password" == password.getAttribute("type")) {
      password.setAttribute("type", "text");
      target.setAttribute("src", "./assets/img/login/eye-disabled.svg");
    } else {
      password.setAttribute("type", "password");
      target.setAttribute("src", "./assets/img/login/eye-enabled.svg");
    }
  };

  ModalSignin.prototype.showSigninForm = function (type) {
    // show selected form
    for (var i = 0; i < this.blocks.length; i++) {
      this.blocks[i].getAttribute("data-type") == type
        ? addClass(this.blocks[i], "cd-signin-modal__block--is-selected")
        : removeClass(this.blocks[i], "cd-signin-modal__block--is-selected");
    }
    //update switcher appearance
    var switcherType = type == "signup" ? "signup" : "login";
    for (var i = 0; i < this.switchers.length; i++) {
      this.switchers[i].getAttribute("data-type") == switcherType
        ? addClass(this.switchers[i], "cd-selected")
        : removeClass(this.switchers[i], "cd-selected");
    }
  };

  var signinModal = document.getElementsByClassName("js-signin-modal")[0];
  if (signinModal) {
    new ModalSignin(signinModal);
  }

  //class manipulations - needed if classList is not supported
  function hasClass(el, className) {
    if (el.classList) return el.classList.contains(className);
    else
      return !!el.className.match(
        new RegExp("(\\s|^)" + className + "(\\s|$)")
      );
  }
  function addClass(el, className) {
    var classList = className.split(" ");
    if (el.classList) el.classList.add(classList[0]);
    else if (!hasClass(el, classList[0])) el.className += " " + classList[0];
    if (classList.length > 1) addClass(el, classList.slice(1).join(" "));
  }
  function removeClass(el, className) {
    var classList = className.split(" ");
    if (el.classList) el.classList.remove(classList[0]);
    else if (hasClass(el, classList[0])) {
      var reg = new RegExp("(\\s|^)" + classList[0] + "(\\s|$)");
      el.className = el.className.replace(reg, " ");
    }
    if (classList.length > 1) removeClass(el, classList.slice(1).join(" "));
  }

  //move-cursor-to-end-of-textarea-or-input
  function putCursorAtEnd(el) {
    if (el.setSelectionRange) {
      var len = el.value.length * 2;
      el.focus();
      el.setSelectionRange(len, len);
    } else {
      el.value = el.value;
    }
  }
})();



// Sign up


setErrorEmpty = (error) => {
  // Text about error
  let errorName = error.placeholder;
  let errorNode = document.createElement("p");
  let errorText = document.createTextNode(`${errorName} cannot be empty`);
  errorNode.appendChild(errorText);
  errorNode.classList.add("error-text");
  error.parentElement.appendChild(errorNode);
};

setErrorFormat = (error) => {
  let errorName = error.placeholder;
  let errorType = errorName.toLowerCase();
  let errorNode = document.createElement("p");
  let errorText;
  if (errorType == "e-mail") {
    errorText = document.createTextNode("Looks like this is not an email");
  }
  if (errorType == "password") {
    errorText = document.createTextNode("Password length is at least 8");
  }
  if (errorType == "confirm password") {
    errorText = document.createTextNode("Password are not matching");
  }
  errorNode.appendChild(errorText);
  errorNode.classList.add("error-text");
  error.parentElement.appendChild(errorNode);
};

removeError = (error) => {
  let errorNode = error.parentElement.querySelector(".error-text");
  error.parentElement.removeChild(errorNode);
};
