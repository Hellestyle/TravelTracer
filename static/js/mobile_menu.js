function toggleMenu() {
  var x = document.getElementById("nav");
  var icon = document.querySelector('.nav-container a.icon i');

  if (x.className === "nav-container") {
    x.className += " responsive";
    icon.classList.remove('fa-bars');
    icon.classList.add('fa-times');
  } else {
    x.className = "nav-container";
    icon.classList.add('fa-bars');
    icon.classList.remove('fa-times');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('click', function (event) {
    var navContainer = document.getElementById('nav');
    var menuIcon = document.querySelector('.nav-container a.icon');

    if (menuIcon.contains(event.target)) {
      toggleMenu();
    } else if (!navContainer.contains(event.target) && navContainer.classList.contains('responsive')) {
      navContainer.classList.remove('responsive');
      document.querySelector('.nav-container a.icon i').classList.add('fa-bars');
      document.querySelector('.nav-container a.icon i').classList.remove('fa-times');
    }
  });
});