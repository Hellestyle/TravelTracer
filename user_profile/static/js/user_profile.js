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
        sideBar.classList.toggle('close');
    });
});

const menuBar = document.querySelector('.content nav .bx.bx-menu-alt-left');
const sideBar = document.querySelector('.sidebar');
menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const settingsButtons = document.querySelectorAll('.content div#settings > button');
const settingsDivs = document.querySelectorAll('.content div#settings > div');

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