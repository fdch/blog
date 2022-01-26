const backIcon  = "⏮";
const lightIcon = "🌝";
const darkIcon  = "🌚";
const backIconText = "Back to blog";
const lightIconText = "Light-mode Switch";
const darkIconText = "Dark-mode Switch";

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");  
const modeBtn = document.querySelector(".mode");
const windowStorage = window.localStorage;
const currentTheme = windowStorage.getItem("theme");

let lightIconDiv = document.createElement("div")
lightIconDiv.innerHTML = lightIcon;
lightIconDiv.setAttribute('title', lightIconText);
lightIconDiv.setAttribute('alt', lightIconText);
let darkIconDiv = document.createElement("div")
darkIconDiv.innerHTML = darkIcon;
darkIconDiv.setAttribute('title', darkIconText);
darkIconDiv.setAttribute('alt', darkIconText);

let currentIcon = darkIconDiv;
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
    currentIcon = lightIconDiv;
  } else if (theme == 0) {
    currentIcon = darkIconDiv;
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

window.onload = () => {
  if (!doneRotation) {
    clearInterval(rotationInterval);
    currentIcon.style.transform = `rotate(0deg)`;
  } else {
    doneRotation = true;
  }
  updateTheme(window.localStorage.getItem("theme"));
  // The back button for the posts page
  const backBtn = document.getElementsByClassName("back");
  
  if (backBtn.length > 0) {
    console.log(backBtn);
    Array.from(backBtn).forEach(b => {
      const backIconSpan = document.createElement("span");
      backIconSpan.innerHTML = backIcon;
      b.setAttribute('title', backIconText);
      b.setAttribute('alt', backIconText);
      b.appendChild(backIconSpan);
      b.onclick = () => {
        document.location.href = "..";
      }
      console.log(b);
    })
  }

};

updateIcon();