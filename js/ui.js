const backIcon  = "⏮";
const lightIcon = "🌝";
const darkIcon  = "🌚";

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");  
const modeBtn = document.querySelector(".mode");
const backBtn = document.querySelector(".back");
const windowStorage = window.localStorage;
const currentTheme = windowStorage.getItem("theme");

let backIconSpan = document.createElement("div")
backIconSpan.innerHTML = backIcon;
let lightIconSpan = document.createElement("div")
lightIconSpan.innerHTML = lightIcon;
let darkIconSpan = document.createElement("div")
darkIconSpan.innerHTML = darkIcon;

let currentIcon = darkIconSpan;
let lastIcon = null;

let rotateAngle = 0;
let doneRotation = false;


rotation = (icon) => {
  if (!doneRotation) {
    rotateAngle += 4;
    icon.style.transform = `rotate(${rotateAngle}deg)`;
  }
}

const rotationInterval = setInterval(() => rotation(currentIcon), 2)

if (currentTheme == 0) {
  document.body.classList.toggle("light-theme");
} else {
  document.body.classList.toggle("dark-theme");
}

updateIcon = (theme) => {
  if (theme == 1) {
    currentIcon = lightIconSpan;
  } else if (theme == 0) {
    currentIcon = darkIconSpan;
  }
  if (lastIcon!==null && modeBtn !== lastIcon) modeBtn.removeChild(modeBtn.firstChild);
  modeBtn.appendChild(currentIcon);
  lastIcon = currentIcon;
}

updateTheme = (prevTheme) => {
  let theme;
  if (prevTheme==null) {
    if (prefersDarkScheme.matches) {
      document.body.classList.toggle("light-theme");
      theme = document.body.classList.contains("light-theme")
      ? 0
      : 1;
    } else {
      document.body.classList.toggle("dark-theme");
      theme = document.body.classList.contains("dark-theme")
      ? 1
      : 0;
    }
  } else {
    theme = prevTheme
  }
  updateIcon(theme);
  localStorage.setItem("theme", theme);
}

// the below code is for the toggle button
modeBtn.onclick = () => {
  updateTheme();
};

// The back button for the posts page
if (backBtn!==null) {
  backBtn.appendChild(backIconSpan);
  backBtn.onclick = () => {
    document.location.href = "../index.html";
  }
}

window.onload = () => {
  if (!doneRotation) {
    clearInterval(rotationInterval);
    currentIcon.style.transform = `rotate(0deg)`;
  } else {
    doneRotation = true;
  }
  updateTheme(window.localStorage.getItem("theme"));
};

updateIcon();