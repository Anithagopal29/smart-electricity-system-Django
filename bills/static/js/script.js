document.getElementById("darkModeToggle").addEventListener("click", function() {
    document.body.classList.toggle("dark-mode");
});

document.getElementById("languageSelect").addEventListener("change", function() {
    alert("Language changed to: " + this.value);
});

document.getElementById("backButton").addEventListener("click", function() {
    window.location.href = "/";
});
