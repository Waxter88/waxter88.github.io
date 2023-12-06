document.addEventListener('DOMContentLoaded', function() {
    feather.replace(); // Initialize Feather Icons

    document.getElementById('nav-toggle').addEventListener('click', function() {
        var navList = document.querySelector('nav ul');
        var nav = document.querySelector('nav');
        navList.classList.toggle('nav-visible'); // Toggle the class
        nav.classList.toggle('nav-visible'); // Toggle the class
        console.log('nav-toggle clicked');
    });

    
    fetch('https://api.github.com/users/Waxter88/repos')
    .then(response => response.json())
    .then(data => {
        const reposContainer = document.getElementById('projects-section');
        data.forEach(repo => {
            const repoElement = document.createElement('a');
            repoElement.className = 'project';
            repoElement.href = repo.html_url;
            repoElement.target = '_blank';
            repoElement.innerHTML = `
                <h3>${repo.name}</h3>
                <p>${repo.description || 'No description available'}</p>
            `;
            reposContainer.appendChild(repoElement);
        });
    })
    .catch(error => console.log('Error fetching GitHub repositories:', error));

    
    var toggleButton = document.getElementById('theme-toggle');
    var themeStyleLink = document.getElementById('theme-style');
    
    if (toggleButton && themeStyleLink) {
        toggleButton.addEventListener('click', function() {
        var currentTheme = document.documentElement.getAttribute('data-theme');
        
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            themeStyleLink.href = 'light-theme.css';
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeStyleLink.href = 'styles.css';
        }
        });
    }

    document.querySelectorAll('.tooltip').forEach(function (tooltip) {
        tooltip.addEventListener('mouseenter', function () {
            var tooltipText = this.querySelector('.tooltiptext');
            var rect = tooltipText.getBoundingClientRect();
            
            // Reset classes
            tooltipText.className = 'tooltiptext';
    
            // Determine the best position for the tooltip
            if (rect.top < 0) {
                tooltipText.classList.add('bottom');
            } else if (window.innerWidth - rect.right < 0) {
                tooltipText.classList.add('left');
            } else if (rect.left < 0) {
                tooltipText.classList.add('right');
            } else {
                tooltipText.classList.add('top');
            }
        });
    });
    
      
});
