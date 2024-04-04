// // Opens sidemenu when you click the menu button
// const menuBarButton = document.querySelector('.content nav .bx.bx-menu-alt-left');
// const sideMenu = document.querySelector('.sidebar');
// menuBarButton.addEventListener('click', () => {
//     sideMenu.classList.toggle('close');
//     editprofilewindow.style.display = "none";
//     editProfileDivs.forEach(div => {
//         div.classList.add('hidden');
//     });
// });

// // Opens the correct content when you select from the sidemenu
// const sideBarMenuOptions = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');
// const contentDivs = document.querySelectorAll('.content > div');
// sideBarMenuOptions.forEach(item => {
//     const li = item.parentElement;
//     item.addEventListener('click', () => {
//         sideBarMenuOptions.forEach(i => {
//             i.parentElement.classList.remove('active');
//         });
//         const itemid = item.id;
//         contentDivs.forEach(b => {
//             if (b.id === itemid){
//                 b.classList.remove('hidden');
//             } else {
//                 b.classList.add('hidden');
//             }
//         });
//         li.classList.add('active');
//         sideMenu.classList.add('close');
//     });
// });

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

// //not currently used
// function toggleDiv(id) {
//     var settingsDiv = document.getElementById(id);
//       // Toggle between 'none' and 'block' for display property
//     settingsDiv.style.display = (settingsDiv.style.display === 'none' || settingsDiv.style.display === '') ? 'block' : 'none';
//     };

// //not currently used
// function openSidebar(id) {
//     document.getElementById("sidebar").style.width = "250px";
//     document.getElementById(id).style.marginLeft = "250px";
// };
// //not currently used
// function closeSidebar(id) {
//     document.getElementById(id).style.width = "0";
//     document.getElementById(id).style.marginLeft= "0";
// }
// //not currently used
// function toggleDivs(divIds) {
//     // Hide all divs initially
//     divIds.forEach(function(id) {
//         var div = document.getElementById(id);
//         if (div) {
//             div.style.display = 'none';
//         }
//     });

//     // Show the first div
//     if (divIds.length > 0) {
//         var firstDiv = document.getElementById(divIds[0]);
//         if (firstDiv) {
//             firstDiv.style.display = 'block';
//         }
//     }
// }