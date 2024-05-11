document.querySelector('.search-button').addEventListener('click', function(event) {
    event.preventDefault();
    var inputBoxValue = document.querySelector('#input-box').value;
    var selectedAge = document.getElementById("age").value;
    var selectedCat = document.getElementById("category_id").value;
    if (inputBoxValue){
        var newHref = url.sight_category.replace('_user_input_', inputBoxValue).replace('_age_', selectedAge).replace('category_id', selectedCat);

    } else {
        var newHref = url.sight_category.replace('_age_', selectedAge).replace('category_id', selectedCat);
        //var newHref = url.sight_category.replace('_user_input_', inputBoxValue).replace('_age_', selectedAge).replace('category_id', selectedCat);
    }
    window.location.href = newHref;
   
  });