// let theme = document.getElementById("theme");

// theme.addEventListener('click', ()=>{

    
//     document.body.classList.toggle('dark-mode');

    

// })



document.addEventListener('DOMContentLoaded', function() {
    // Check if user has saved a theme preference
    const savedTheme = localStorage.getItem('theme');
    
    // If saved theme is 'dark', apply dark mode
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
});

// === THEME TOGGLE ===
let theme = document.getElementById("theme");

theme.addEventListener('click', ()=>{
    // Toggle dark mode on/off
    document.body.classList.toggle('dark-mode');
    
    // Save the user's preference
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});