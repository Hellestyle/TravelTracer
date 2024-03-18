document.getElementById("sendButton").addEventListener("click", function () {
  let selectedAge = document.getElementById("age").value;
  let newHref = "/sight/sight/age/" + selectedAge;
  window.location.href = newHref;
});
