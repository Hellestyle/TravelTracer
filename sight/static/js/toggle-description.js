function toggleDescription() {
  
    let sightDescription = document.getElementsByClassName('sight-description')[0];

    let sightDescriptionButton = document.getElementsByClassName('sight-description-button')[0];

    if (sightDescription.classList.contains("expanded")) {

        sightDescription.classList.remove("expanded");
        sightDescriptionButton.innerHTML = "...Show more";

    } else {

        sightDescription.classList.add("expanded");
        sightDescriptionButton.innerHTML = "Show less";
    }

}
