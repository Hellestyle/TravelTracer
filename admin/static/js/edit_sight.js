document.addEventListener('DOMContentLoaded', (event) => {  var dragSrcEl = null;

    function handleDragStart(e) {
        this.style.opacity = '0.4';

        dragSrcEl = this;    
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.innerHTML);
    }

    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }

    function handleDragEnter(e) {
        this.classList.add('over');
    }

    function handleDragLeave(e) {
        this.classList.remove('over');
    }

    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation(); // stops the browser from redirecting.
        }
        
        if (dragSrcEl != this) {
            dragSrcEl.innerHTML = this.innerHTML;
            this.innerHTML = e.dataTransfer.getData('text/html');
        }
        
        let orderedBoxes = document.querySelectorAll('.ms-box div[data-value="true"]');
        let orderList = Array.from(orderedBoxes).map(function(box) {return box.innerHTML;}).join(',');
        let input = document.querySelector('input[data-input="drag-order"]');
        input.value = orderList;

        items.forEach(item => {
            item.classList.remove('over')
            item.style.opacity = '1'
        })

        return false;
    }

    function handleDragEnd(e) {
        this.style.opacity = '1';

        items.forEach(function (item) {
            item.classList.remove('over');
        });
    }

    let items = document.querySelectorAll('.ms-boxes .ms-box');
    items.forEach(function(item) {
    item.addEventListener('dragstart', handleDragStart, false);
    item.addEventListener('dragenter', handleDragEnter, false);
    item.addEventListener('dragover', handleDragOver, false);
    item.addEventListener('dragleave', handleDragLeave, false);
    item.addEventListener('drop', handleDrop, false);
    item.addEventListener('dragend', handleDragEnd, false);
    });  
    // Set initial value of the input field
    let orderedBoxes = document.querySelectorAll('.ms-box div[data-value="true"]');
    let orderList = Array.from(orderedBoxes).map(function(box) {return box.innerHTML;}).join(',');
    let input = document.querySelector('input[data-input="drag-order"]');
    input.value = orderList;

});
