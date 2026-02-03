/**
 * Minimal Portfolio - Main Script
 * Modern, performant JavaScript with ES6+
 */

// Configuration
const CONFIG = {
    github: {
        username: 'waxter88',
        reposToShow: 6
    },
    theme: {
        storageKey: 'theme-preference',
        default: 'dark'
    }
};

// Language Colors (GitHub official colors)
const LANGUAGE_COLORS = {
    JavaScript: '#f1e05a',
    TypeScript: '#3178c6',
    Python: '#3572A5',
    HTML: '#e34c26',
    CSS: '#563d7c',
    Java: '#b07219',
    'C++': '#f34b7d',
    C: '#555555',
    Go: '#00ADD8',
    Rust: '#dea584',
    Ruby: '#701516',
    PHP: '#4F5D95',
    Swift: '#F05138',
    Kotlin: '#A97BFF',
    Vue: '#41b883',
    Shell: '#89e051',
    'C#': '#178600'
};

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initCursorGlow();
    initMobileMenu();
    initScrollEffects();
    initRevealAnimations();
    fetchGitHubData();
    updateFooterYear();
});

/**
 * Theme Toggle
 * Supports dark/light mode with system preference detection
 */
function initTheme() {
    const toggle = document.getElementById('theme-toggle');
    const metaTheme = document.getElementById('theme-color-meta');
    
    // Get stored preference or default to dark
    const getPreference = () => {
        const stored = localStorage.getItem(CONFIG.theme.storageKey);
        if (stored) return stored;
        
        // Optional: Check system preference (but default to dark)
        // return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
        return CONFIG.theme.default;
    };
    
    // Apply theme to document
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(CONFIG.theme.storageKey, theme);
        
        // Update meta theme-color for mobile browsers
        if (metaTheme) {
            metaTheme.setAttribute('content', theme === 'dark' ? '#0d0d0d' : '#fafafa');
        }
    };
    
    // Initialize theme
    setTheme(getPreference());
    
    // Toggle handler
    if (toggle) {
        toggle.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            setTheme(next);
        });
    }
    
    // Listen for system preference changes (optional)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // Only auto-switch if user hasn't set a preference
        if (!localStorage.getItem(CONFIG.theme.storageKey)) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * Cursor Glow Effect
 * Follows mouse for subtle ambient lighting
 */
function initCursorGlow() {
    const glow = document.querySelector('.cursor-glow');
    if (!glow) return;

    let mouseX = 0, mouseY = 0;
    let currentX = 0, currentY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animate() {
        // Smooth follow with easing
        currentX += (mouseX - currentX) * 0.1;
        currentY += (mouseY - currentY) * 0.1;
        
        glow.style.left = `${currentX}px`;
        glow.style.top = `${currentY}px`;
        
        requestAnimationFrame(animate);
    }
    
    animate();
}

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const toggle = document.querySelector('.nav__toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileLinks = document.querySelectorAll('.mobile-menu__link');
    const body = document.body;

    if (!toggle || !mobileMenu) return;

    toggle.addEventListener('click', () => {
        toggle.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });

    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            toggle.classList.remove('active');
            mobileMenu.classList.remove('active');
            body.style.overflow = '';
        });
    });
}

/**
 * Scroll Effects
 * Header background on scroll
 */
function initScrollEffects() {
    const header = document.querySelector('.header');
    
    if (!header) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Initial check
}

/**
 * Reveal Animations
 * Intersection Observer for scroll reveal
 */
function initRevealAnimations() {
    const revealElements = document.querySelectorAll('.reveal');
    
    if (!revealElements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
}

/**
 * GitHub API Integration
 * Fetch profile and repositories
 */
async function fetchGitHubData() {
    try {
        const { username, reposToShow } = CONFIG.github;
        
        // Fetch user data and repos in parallel
        const [userResponse, reposResponse] = await Promise.all([
            fetch(`https://api.github.com/users/${username}`),
            fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`)
        ]);

        if (!userResponse.ok || !reposResponse.ok) {
            throw new Error('GitHub API request failed');
        }

        const userData = await userResponse.json();
        const reposData = await reposResponse.json();

        // Update profile
        updateGitHubProfile(userData, reposData);
        
        // Update repos grid
        updateReposGrid(reposData);

    } catch (error) {
        console.error('Error fetching GitHub data:', error);
        showGitHubError();
    }
}

/**
 * Update GitHub Profile Section
 */
function updateGitHubProfile(user, repos) {
    // Avatar
    const avatarContainer = document.querySelector('.github-avatar');
    if (avatarContainer && user.avatar_url) {
        avatarContainer.innerHTML = `<img src="${user.avatar_url}" alt="${user.login}" loading="lazy">`;
    }

    // Bio
    const bioElement = document.querySelector('.github-bio');
    if (bioElement && user.bio) {
        bioElement.textContent = user.bio;
    }

    // Stats
    const repoCount = document.getElementById('repo-count');
    const followerCount = document.getElementById('follower-count');
    const starCount = document.getElementById('star-count');

    if (repoCount) repoCount.textContent = user.public_repos || 0;
    if (followerCount) followerCount.textContent = user.followers || 0;

    // Calculate total stars
    if (starCount) {
        const totalStars = repos.reduce((acc, repo) => acc + (repo.stargazers_count || 0), 0);
        starCount.textContent = totalStars;
    }
}

/**
 * Update Repos Grid
 */
function updateReposGrid(repos) {
    const grid = document.querySelector('.repos-grid');
    if (!grid) return;

    // Filter and sort repos
    const filteredRepos = repos
        .filter(repo => !repo.fork && !repo.archived)
        .sort((a, b) => {
            // Sort by stars, then by recent update
            if (b.stargazers_count !== a.stargazers_count) {
                return b.stargazers_count - a.stargazers_count;
            }
            return new Date(b.updated_at) - new Date(a.updated_at);
        })
        .slice(0, CONFIG.github.reposToShow);

    grid.innerHTML = filteredRepos.map(repo => createRepoCard(repo)).join('');
}

/**
 * Create Repo Card HTML
 */
function createRepoCard(repo) {
    const langColor = LANGUAGE_COLORS[repo.language] || '#858585';
    const description = repo.description || 'No description available';
    
    return `
        <a href="${repo.html_url}" class="repo-card" target="_blank" rel="noopener noreferrer">
            <div class="repo-card__header">
                <svg class="repo-card__icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8z" fill="currentColor"/>
                </svg>
                <h3 class="repo-card__name">${repo.name}</h3>
            </div>
            <p class="repo-card__description">${escapeHtml(description)}</p>
            <div class="repo-card__meta">
                ${repo.language ? `
                    <span class="repo-card__stat">
                        <span class="language-dot" style="background: ${langColor}"></span>
                        ${repo.language}
                    </span>
                ` : ''}
                <span class="repo-card__stat">
                    <svg viewBox="0 0 16 16" fill="currentColor">
                        <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
                    </svg>
                    ${repo.stargazers_count}
                </span>
                <span class="repo-card__stat">
                    <svg viewBox="0 0 16 16" fill="currentColor">
                        <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75v-.878a2.25 2.25 0 111.5 0v.878a2.25 2.25 0 01-2.25 2.25h-1.5v2.128a2.251 2.251 0 11-1.5 0V8.5h-1.5A2.25 2.25 0 013.5 6.25v-.878a2.25 2.25 0 111.5 0zM5 3.25a.75.75 0 10-1.5 0 .75.75 0 001.5 0zm6.75.75a.75.75 0 100-1.5.75.75 0 000 1.5zm-3 8.75a.75.75 0 10-1.5 0 .75.75 0 001.5 0z"/>
                    </svg>
                    ${repo.forks_count}
                </span>
            </div>
        </a>
    `;
}

/**
 * Show GitHub Error State
 */
function showGitHubError() {
    const grid = document.querySelector('.repos-grid');
    if (grid) {
        grid.innerHTML = `
            <div class="repo-card" style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <p style="color: var(--text-tertiary);">Unable to load repositories. Please check back later.</p>
            </div>
        `;
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Update Footer Year
 */
function updateFooterYear() {
    const yearElement = document.getElementById('year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

/**
 * Smooth Scroll Polyfill for Safari
 */
if (!CSS.supports('scroll-behavior', 'smooth')) {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}
