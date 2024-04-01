function switchPage(parentId, page) {

    let parent = document.getElementById(parentId);

    let containers = parent.getElementsByClassName('sight-container');

    let paginationButtons = parent.getElementsByClassName('pagination-button');

    for (let i = 0; i < containers.length; i++) {
        if ((page - 1) * 2 <= i && i < page * 2) {
            containers[i].style.display = "block";
        } else {
            containers[i].style.display = "none";
        }
    }

    for (let i = 0; i < paginationButtons.length; i++) {
        paginationButtons[i].classList.remove('pagination-button-active');
    }

    paginationButtons[page-1].classList.add('pagination-button-active');

}

function previousPage(parentId) {

    let parent = document.getElementById(parentId);

    let currentPage = Number(parent.getElementsByClassName('pagination-button-active')[0].innerText);

    if (currentPage > 1) {
        switchPage(parentId, currentPage - 1);
    }

}

function nextPage(parentId) {

    let parent = document.getElementById(parentId);
    
    let currentPage = Number(parent.getElementsByClassName('pagination-button-active')[0].innerText);

    let numberOfContainers = parent.getElementsByClassName('sight-container').length;
    
    if (currentPage < Math.ceil(numberOfContainers / 2)) {
        switchPage(parentId, currentPage + 1);
    }
    
}
