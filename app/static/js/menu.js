const menuButton = document.getElementById("menu-button");
const closeButton = document.getElementById("close-button");
const popupMenu = document.getElementById("popup-menu");
const overlay = document.getElementById("overlay");

menuButton.addEventListener("click", () => {
  popupMenu.classList.toggle("hidden");
  overlay.classList.toggle("active");
});

closeButton.addEventListener("click", () => {
  popupMenu.classList.add("hidden");
  overlay.classList.remove("active");
});

// Close the popup if clicking outside of it
overlay.addEventListener("click", () => {
  popupMenu.classList.add("hidden");
  overlay.classList.remove("active");
});