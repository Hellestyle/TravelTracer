// Opens sidemenu when you click the menu button
const menuBarButton = document.querySelector(
  ".content nav .bx.bx-menu-alt-left"
);
const sideMenu = document.querySelector(".sidebar");
menuBarButton.addEventListener("click", () => {
  sideMenu.classList.toggle("close");
  editprofilewindow.style.display = "none";
  editProfileDivs.forEach((div) => {
    div.classList.add("hidden");
  });
});

// Opens the correct content when you select from the sidemenu
/*
const sideBarMenuOptions = document.querySelectorAll(
  ".sidebar .side-menu li a:not(.logout)"
);
const contentDivs = document.querySelectorAll(".content > div");
sideBarMenuOptions.forEach((item) => {
  const li = item.parentElement;
  item.addEventListener("click", () => {
    sideBarMenuOptions.forEach((i) => {
      i.parentElement.classList.remove("active");
    });
    const itemid = item.id;
    contentDivs.forEach((b) => {
      if (b.id === itemid) {
        b.classList.remove("hidden");
      } else {
        b.classList.add("hidden");
      }
    });
    li.classList.add("active");
    sideMenu.classList.add("close");
  });
});
*/

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target != menuBarButton){
      sideMenu.classList.add('close');
  }
}

function switchPage(page) {
  let containers = document.getElementsByClassName("container");

  let paginationButtons = document.getElementsByClassName("pagination-button");

  for (let i = 0; i < containers.length; i++) {
    if ((page - 1) * 3 <= i && i < page * 3) {
      containers[i].style.display = "block";
    } else {
      containers[i].style.display = "none";
    }
  }

  for (let i = 0; i < paginationButtons.length; i++) {
    paginationButtons[i].classList.remove("pagination-button-active");
  }

  paginationButtons[page - 1].classList.add("pagination-button-active");
}

function previousPage() {
  let currentPage = Number(
    document.getElementsByClassName("pagination-button-active")[0].innerText
  );

  if (currentPage > 1) {
    switchPage(currentPage - 1);
  }
}

function nextPage() {
  let currentPage = Number(
    document.getElementsByClassName("pagination-button-active")[0].innerText
  );

  let numberOfContainers = document.getElementsByClassName("container").length;

  if (currentPage < Math.ceil(numberOfContainers / 3)) {
    switchPage(currentPage + 1);
  }
}
