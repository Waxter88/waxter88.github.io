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

    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            var currentTheme = document.documentElement.getAttribute('data-theme');
            
            if (currentTheme === 'light') {
                document.documentElement.setAttribute('data-theme', 'dark');
                toggleButton.innerHTML = '☀️';
            } else if(currentTheme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                toggleButton.innerHTML = '🌙';
            }
        });
    }
        
    document.getElementById('about-toggle').addEventListener('click', function() {
        var moreText = document.getElementById('more-about');
        if (moreText.style.display === "none") {
            moreText.style.display = "block";
            this.innerHTML = "Read Less " + feather.icons['chevron-up'].toSvg();   
        } else {
            moreText.style.display = "none";
            this.innerHTML = "Read More " + feather.icons['chevron-down'].toSvg();
        }
    });
    
      
});
