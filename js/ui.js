const backIcon = "⏮";
const lightIcon = "🌝";
const darkIcon = "🌚";

const btn = document.querySelector(".btn-toggle");
const backButton = document.querySelector(".back");

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
const currentTheme = localStorage.getItem("theme");

if (currentTheme == "dark") {
  document.body.classList.toggle("dark-theme");
  btn.innerHTML = lightIcon;
} else if (currentTheme == "light") {
  document.body.classList.toggle("light-theme");
  btn.innerHTML = darkIcon;
}

// the below code is for the toggle button
btn.addEventListener("click", function () {
  if (prefersDarkScheme.matches) {
    document.body.classList.toggle("light-theme");
    var theme = document.body.classList.contains("light-theme")
      ? "light"
      : "dark";
    } else {
      document.body.classList.toggle("dark-theme");
      var theme = document.body.classList.contains("dark-theme")
      ? "dark"
      : "light";
  }
  localStorage.setItem("theme", theme);
  if (theme == "dark") {
    btn.innerHTML = lightIcon;
  } else if (theme == "light") {
    btn.innerHTML = darkIcon;
  }
});

// The back button for the posts page
if (backButton!==null) {
  backButton.addEventListener('click', function () {
    document.location.href = "../index.html";
  });
}
