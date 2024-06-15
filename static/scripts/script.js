// static/scripts/script.js

function toggleNav() {
            var nav = document.getElementById("nav-links");
            if (nav.style.display === "block" || nav.style.display === "") {
                nav.style.display = "none";
            } else {
                nav.style.display = "block";
            }
        }