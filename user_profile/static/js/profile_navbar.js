function switchNavbar(navbarItem) {

    let navbarItems = document.getElementsByClassName('profile-nav-button');
    let profileBodies = document.getElementsByClassName('profile-body');
    
    let navbarButton = document.getElementById(`profile-nav-button-${navbarItem}`);

    let profileBodyContainer = document.getElementById(`profile-body-${navbarItem}`);
    
    for (let i = 0; i < navbarItems.length; i++) {
        navbarItems[i].classList.remove('profile-nav-button-active');
    }

    for (let i = 0; i < profileBodies.length; i++) {
        profileBodies[i].classList.add('hidden');
    }

    navbarButton.classList.add('profile-nav-button-active');

    profileBodyContainer.classList.remove('hidden');

}
