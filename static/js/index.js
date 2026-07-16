function toggleExpandable(panelId, toggleButtonSelector, toggleTextSelector) {
    const panel = document.getElementById(panelId);
    const toggleButton = document.querySelector(toggleButtonSelector);
    const toggleText = document.querySelector(toggleTextSelector);

    if (!panel || !toggleButton || !toggleText) {
        return;
    }

    if (panel.classList.contains('expanded')) {
        panel.classList.remove('expanded');
        toggleButton.classList.remove('expanded');
        toggleText.textContent = 'Click to View More';
    } else {
        panel.classList.add('expanded');
        toggleButton.classList.add('expanded');
        toggleText.textContent = 'Click to View Less';
    }
}

function toggleRollouts() {
    toggleExpandable('rolloutsPanel', '.expandable-toggle', '.rollout-toggle-text');
}

// =================================
// NAVIGATION SYSTEM FUNCTIONALITY
// =================================

class NavigationManager {
    constructor() {
        this.sections = ['introduction', 'abstract', 'method', 'results', 'rollouts', 'citation'];
        this.navLinks = {
            desktop: document.querySelectorAll('.nav-link'),
            mobile: document.querySelectorAll('.nav-link-mobile')
        };
        this.mobileMenuToggle = document.getElementById('mobileMenuToggle');
        this.mobileMenuClose = document.getElementById('mobileMenuClose');
        this.mobileOverlay = document.getElementById('mobileOverlay');
        this.currentSection = 'introduction';
        
        this.init();
    }
    
    init() {
        this.setupScrollSpy();
        this.setupSmoothScrolling();
        this.setupMobileMenu();
        this.updateActiveNavigation('introduction');
        
        // Initial scroll spy check
        setTimeout(() => this.handleScroll(), 100);
    }
    
    setupScrollSpy() {
        let ticking = false;
        
        const handleScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    this.handleScroll();
                    ticking = false;
                });
                ticking = true;
            }
        };
        
        window.addEventListener('scroll', handleScroll);
    }
    
    handleScroll() {
        const scrollPosition = window.scrollY + 100; // Offset for fixed nav
        let activeSection = this.sections[0];
        
        // Find the current section based on scroll position
        for (const sectionId of this.sections) {
            const section = document.getElementById(sectionId);
            if (section && section.offsetTop <= scrollPosition) {
                activeSection = sectionId;
            }
        }
        
        // Update active navigation if section changed
        if (activeSection !== this.currentSection) {
            this.currentSection = activeSection;
            this.updateActiveNavigation(activeSection);
        }
    }
    
    updateActiveNavigation(activeSection) {
        // Update desktop navigation
        this.navLinks.desktop.forEach(link => {
            const target = link.dataset.target;
            if (target === activeSection) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
        
        // Update mobile navigation
        this.navLinks.mobile.forEach(link => {
            const target = link.dataset.target;
            if (target === activeSection) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
    
    setupSmoothScrolling() {
        // Handle desktop navigation clicks
        this.navLinks.desktop.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.dataset.target;
                this.scrollToSection(targetId);
            });
        });
        
        // Handle mobile navigation clicks
        this.navLinks.mobile.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.dataset.target;
                this.scrollToSection(targetId);
                this.closeMobileMenu();
            });
        });
    }
    
    scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const isMobile = window.innerWidth <= 1024;
            const offset = isMobile ? 80 : 20; // Account for mobile header
            const targetPosition = section.offsetTop - offset;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
            
            // Update active state immediately for better UX
            this.currentSection = sectionId;
            this.updateActiveNavigation(sectionId);
        }
    }
    
    setupMobileMenu() {
        // Toggle mobile menu
        this.mobileMenuToggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMobileMenu();
        });
        
        // Close mobile menu
        this.mobileMenuClose.addEventListener('click', (e) => {
            e.preventDefault();
            this.closeMobileMenu();
        });
        
        // Close menu when clicking overlay
        this.mobileOverlay.addEventListener('click', (e) => {
            if (e.target === this.mobileOverlay) {
                this.closeMobileMenu();
            }
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.mobileOverlay.classList.contains('active')) {
                this.closeMobileMenu();
            }
        });
    }
    
    toggleMobileMenu() {
        const isActive = this.mobileOverlay.classList.contains('active');
        if (isActive) {
            this.closeMobileMenu();
        } else {
            this.openMobileMenu();
        }
    }
    
    openMobileMenu() {
        this.mobileOverlay.classList.add('active');
        this.mobileMenuToggle.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
    
    closeMobileMenu() {
        this.mobileOverlay.classList.remove('active');
        this.mobileMenuToggle.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Initialize Navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NavigationManager();
});
