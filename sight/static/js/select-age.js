document.querySelector('.search-button').addEventListener('click', function(event) {
  event.preventDefault();
  var inputBoxValue = document.querySelector('#input-box').value;

  // ages is always selected, either "all" or other age categories
  var selectedAge = document.getElementById("age").value;

  // If the input box is not empty and age is either "all" or other age categories
  if (inputBoxValue && selectedAge) {
    var newHref = url.sight_category.replace('_category_', inputBoxValue).replace('_age_', selectedAge);
    window.location.href = newHref;
  } else {
    // If the input box is empty but the age is either "all" or other age categories
    var newHref = url.age_category.replace('_age_', selectedAge);
    window.location.href = newHref;
  }
});