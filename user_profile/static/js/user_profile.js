const menuBar = document.querySelector('.content nav .bx.bx-menu-alt-left');
const sideBar = document.querySelector('.sidebar');
menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
    modal.style.display = "none";
    settingsDivs.forEach(div => {
        div.classList.add('hidden');
    });
});

const sideBarMenuOptions = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');
const contentDivs = document.querySelectorAll('.content > div');

sideBarMenuOptions.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideBarMenuOptions.forEach(i => {
            i.parentElement.classList.remove('active');
        });
        const itemid = item.id;
        contentDivs.forEach(b => {
            if (b.id === itemid){
                b.classList.remove('hidden');
            } else {
                b.classList.add('hidden');
            }
        });
        li.classList.add('active');
        sideBar.classList.add('close');
    });
});

const editprofilebutton = document.querySelector('.content #profile .profile-header .profile-info #edit-profile-settings ');
var modal = document.querySelector(".content div#profile div.modal");
var span = document.querySelector('.content div#profile div.modal span.close')

console.log(editprofilebutton);
console.log(modal);
editprofilebutton.addEventListener('click', () => {
    modal.style.display = "block"
});

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
  }
  
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
if (event.target == modal) {
    modal.style.display = "none";
}
}





const settingsButtons = document.querySelectorAll('.content #profile div#edit-profile-settings div > button');
const settingsDivs = document.querySelectorAll('.content #profile div#edit-profile-settings div > div');

settingsButtons.forEach(button => {
    button.addEventListener('click', () => {
        settingsDivs.forEach(div => {
            if (div.id === button.id) {
                div.classList.toggle('hidden');
            } else {
                div.classList.add('hidden');
            };
        });
    });
});

//not currently used
function toggleDiv(id) {
    var settingsDiv = document.getElementById(id);
      // Toggle between 'none' and 'block' for display property
    settingsDiv.style.display = (settingsDiv.style.display === 'none' || settingsDiv.style.display === '') ? 'block' : 'none';
    };

//not currently used
function openSidebar(id) {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById(id).style.marginLeft = "250px";
};
//not currently used
function closeSidebar(id) {
    document.getElementById(id).style.width = "0";
    document.getElementById(id).style.marginLeft= "0";
}
//not currently used
function toggleDivs(divIds) {
    // Hide all divs initially
    divIds.forEach(function(id) {
        var div = document.getElementById(id);
        if (div) {
            div.style.display = 'none';
        }
    });

    // Show the first div
    if (divIds.length > 0) {
        var firstDiv = document.getElementById(divIds[0]);
        if (firstDiv) {
            firstDiv.style.display = 'block';
        }
    }
}