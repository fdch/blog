const btn = document.querySelector(".btn-toggle");
const backButton = document.querySelector(".back");
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
const currentTheme = localStorage.getItem("theme");
const postsSection = document.querySelector("#posts");
const w = window.innerWidth 
          || document.documentElement.clientWidth 
          || document.body.clientWidth 
          || 0;
postsSection.setAttribute('style', `width: ${w}px;`);
postsSection.style.width = `${w}px`;

if (currentTheme == "dark") {
  document.body.classList.toggle("dark-theme");
  btn.innerHTML = "🌝";
} else if (currentTheme == "light") {
  document.body.classList.toggle("light-theme");
  btn.innerHTML = "🌚";
}

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
    btn.innerHTML = "🌝";
  } else if (theme == "light") {
    btn.innerHTML = "🌚";
  }
});
// The back button for the posts page
if (backButton!==null) {
  backButton.addEventListener('click', function () {
    document.location.href="../index.html"
  });
}
