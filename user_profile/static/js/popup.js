function openPopup(likeUrl, dislikeUrl, closeUrl) {

    let popupBackground = document.getElementById("popup-background");

    let popup = document.getElementById("popup");

    let likeButton = popup.getElementsByClassName("button-like")[0];
    let dislikeButton = popup.getElementsByClassName("button-dislike")[0];

    let closeButton = popup.getElementsByClassName("close-button")[0];

    popupBackground.addEventListener("click", function(event) {
        if (event.target === popupBackground) {
            closePopup(closeUrl);
        }
    });

    likeButton.href = likeUrl;
    dislikeButton.href = dislikeUrl;

    closeButton.addEventListener("click", function() {
        closePopup(closeUrl);
    });

    popupBackground.style.display = "block";
}

function closePopup(url) {

    document.getElementById("popup-background").style.display = "none";

    $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {
            window.location.reload();
        }
    });

}
