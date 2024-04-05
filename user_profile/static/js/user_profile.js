
// Opens the editprofile modal when you click the editprofile button
const editprofilebutton = document.querySelector('.content #profile .profile-header .profile-info #edit-profile-settings ');
const editprofilewindow = document.querySelector(".content div#profile div.modal");
const editprofilemodalclosebutton = document.querySelector('.content div#profile div.modal span.close-modal')
editprofilebutton.addEventListener('click', () => {
    editprofilewindow.style.display = "block"
});

// Opens content belonging to the buttons inside editprofile modal
const editProfileButtons = document.querySelectorAll('.content #profile div#edit-profile-settings div > button');
const editProfileDivs = document.querySelectorAll('.content #profile div#edit-profile-settings div > div');
editProfileButtons.forEach(button => {
    button.addEventListener('click', () => {
        editProfileDivs.forEach(div => {
            if (div.id === button.id) {
                div.classList.toggle('hidden');
            } else {
                div.classList.add('hidden');
            };
        });
    });
});

// When the user clicks on <span> (x), close the modal
editprofilemodalclosebutton.onclick = function() {
    editprofilewindow.style.display = "none";
}
  
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == editprofilewindow) {
        editprofilewindow.style.display = "none";
        editProfileDivs.forEach(div => {
            div.classList.add('hidden');
        });
    }
    if (event.target != menuBarButton){
        sideMenu.classList.add('close');
    }
}

// Allows alerts to be dismissed
const alerts = document.querySelectorAll(".content .container > div.alert")
const dismissAlertButton = document.querySelectorAll(".content .container .alert button.close")
dismissAlertButton.forEach(dismissButton => {
    if (dismissButton) {
        dismissButton.addEventListener("click", (event) => {
            alerts.forEach(alert => {
                if (alert == dismissButton.parentElement) {
                    alert.classList.add("alert-hidden")
                }
            })
        })
    }    
})
