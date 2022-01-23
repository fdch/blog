const backIcon  = "⏮";
const lightIcon = "🌝";
const darkIcon  = "🌚";

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");  
const btn = document.querySelector(".btn-toggle");
const backButton = document.querySelector(".back");
const currentTheme = localStorage.getItem("theme");

let backIconSpan = document.createElement("div")
backIconSpan.innerHTML = backIcon;
let lightIconSpan = document.createElement("div")
lightIconSpan.innerHTML = lightIcon;
let darkIconSpan = document.createElement("div")
darkIconSpan.innerHTML = darkIcon;

let currentIcon = lightIconSpan;

updateIcon = (theme) => {
  lastIcon = currentIcon;
  if (theme == "dark") {
    currentIcon = lightIconSpan;
  } else if (theme == "light") {
    currentIcon = darkIconSpan;
  }
  if (btn.firstChild === lastIcon) btn.removeChild(btn.firstChild);
  btn.appendChild(currentIcon);
}

if (currentTheme == "light") {
  document.body.classList.toggle("light-theme");
} else {
  document.body.classList.toggle("dark-theme");
}

updateIcon()

// the below code is for the toggle button
btn.addEventListener("click", function () {
  let theme;
  if (prefersDarkScheme.matches) {
    document.body.classList.toggle("light-theme");
    theme = document.body.classList.contains("light-theme")
      ? "light"
      : "dark";
    } else {
      document.body.classList.toggle("dark-theme");
      theme = document.body.classList.contains("dark-theme")
      ? "dark"
      : "light";
  }
  updateIcon(theme);
  localStorage.setItem("theme", theme);
});

// The back button for the posts page
if (backButton!==null) {
  backButton.addEventListener('click', function () {
    document.location.href = "../index.html";
  });
}
let rotateAngle = 0;

rotation = () => {
  rotateAngle += 4;
  currentIcon.style.transform = `rotate(${rotateAngle}deg)`;
}

rotationInterval = setInterval(() => rotation(), 2)

window.onload = () => {
  clearInterval(rotationInterval);
  currentIcon.style.transform = `rotate(0deg)`;
};
