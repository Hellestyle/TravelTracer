function switchPage(page) {

    let containers = document.getElementsByClassName('container');

    let paginationButtons = document.getElementsByClassName('pagination-button');

    for (let i = 0; i < containers.length; i++) {
        if ((page - 1) * 3 <= i && i < page * 3) {
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

function previousPage() {

    let currentPage = Number(document.getElementsByClassName('pagination-button-active')[0].innerText);

    if (currentPage > 1) {
        switchPage(currentPage - 1);
    }

}

function nextPage() {
    
    let currentPage = Number(document.getElementsByClassName('pagination-button-active')[0].innerText);

    let numberOfContainers = document.getElementsByClassName('container').length;
    
    if (currentPage < Math.ceil(numberOfContainers / 3)) {
        switchPage(currentPage + 1);
    }
    
}
