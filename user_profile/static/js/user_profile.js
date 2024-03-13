const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        if (sideBar.classList.contains('close')) {
            
        } else {
            sideLinks.forEach(i => {
                i.parentElement.classList.remove('active');
            })
            li.classList.add('active');
            sideBar.classList.toggle('close');
        }
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu-alt-left');
const sideBar = document.querySelector('.sidebar');
sideBar.classList.toggle('close');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

function toggleDiv(id) {
      var settingsDiv = document.getElementById(id);
      // Toggle between 'none' and 'block' for display property
      settingsDiv.style.display = (settingsDiv.style.display === 'none' || settingsDiv.style.display === '') ? 'block' : 'none';
    }

//not currently used
function openSidebar(id) {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById(id).style.marginLeft = "250px";
}
//not currently used
function closeSidebar(id) {
    document.getElementById(id).style.width = "0";
    document.getElementById(id).style.marginLeft= "0";
}

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