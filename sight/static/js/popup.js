function openPopup() {
    document.getElementById("popup-background").style.display = "block";
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
