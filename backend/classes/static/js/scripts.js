// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('menuButton');
    const menu = document.getElementById('menu');

    menuButton.addEventListener('click', () => {
        menu.classList.toggle('show');
    });
});
