function myFunction() {
    var x = document.getElementById("nav");
    if (x.className === "nav-container") {
      x.className += " responsive";
    } else {
      x.className = "nav-container";
    }
  }