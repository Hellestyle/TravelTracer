function handleButtonClick(event, action) {
    event.preventDefault();

    let username = event.target
      .closest("tr")
      .querySelector(".username-data > a").textContent;

    let newUrl;
    if (action == "remove_friend") {
      newUrl = urls[action].replace("_friend_name_", username);
    } else if (action == "cancel_friend_request") {
      newUrl = urls[action].replace("_receiver_name_", username);
    } else {
      newUrl = urls[action].replace("_sender_name_", username);
    }
    window.location.href = newUrl;
  }

  document.querySelectorAll(".accept-button").forEach(function (button) {
    button.addEventListener("click", function (event) {
      handleButtonClick(event, "accept_friend_request");
    });
  });

  document.querySelectorAll(".decline-button").forEach(function (button) {
    button.addEventListener("click", function (event) {
      handleButtonClick(event, "decline_friend_request");
    });
  });

  document.querySelectorAll(".remove-button").forEach(function (button) {
    button.addEventListener("click", function (event) {
      handleButtonClick(event, "remove_friend");
    });
  });

  document.querySelectorAll(".cancel-button").forEach(function (button) {
    button.addEventListener("click", function (event) {
      handleButtonClick(event, "cancel_friend_request");
    });
  });

  document
    .querySelector(".send-friend-request-button")
    .addEventListener("click", function (event) {
      event.preventDefault();

      let receiver_name = document.querySelector(
        ".send-friend-request-input"
      ).value;

      let newUrl = urls["send_friend_request"].replace(
        "_receiver_name_",
        receiver_name
      );
      window.location.href = newUrl;
    });