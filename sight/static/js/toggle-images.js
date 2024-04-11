function showImage(index) {
  var imageElement1 = document.getElementById("image1");
  var imageElement2 = document.getElementById("image2");

  if (index < 0) {
    index = images.length - 1;
  } else if (index >= images.length) {
    index = 0;
  }
  index1 = index;
  index2 = (index1 + 1) % images.length;
  imageElement1.src = images[index1];
  imageElement2.src = images[index2];
}

function prevImage() {
  index1 = (index1 - 1 + images.length) % images.length;
  index2 = (index2 - 1 + images.length) % images.length;
  document.getElementById("image1").src = images[index1];
  document.getElementById("image2").src = images[index2];
}

function nextImage() {
  index1 = (index1 + 1) % images.length;
  index2 = (index2 + 1) % images.length;
  document.getElementById("image1").src = images[index1];
  document.getElementById("image2").src = images[index2];
}
