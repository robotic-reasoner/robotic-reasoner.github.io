window.HELP_IMPROVE_VIDEOJS = false;

var INTERP_BASE = "./static/interpolation/stacked";
var NUM_INTERP_FRAMES = 240;

var interp_images = [];
function preloadInterpolationImages() {
  for (var i = 0; i < NUM_INTERP_FRAMES; i++) {
    var path = INTERP_BASE + '/' + String(i).padStart(6, '0') + '.jpg';
    interp_images[i] = new Image();
    interp_images[i].src = path;
  }
}

function setInterpolationImage(i) {
  var image = interp_images[i];
  image.ondragstart = function() { return false; };
  image.oncontextmenu = function() { return false; };
  $('#interpolation-image-wrapper').empty().append(image);
}


$(document).ready(function() {
    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");

    });

    var options = {
			slidesToScroll: 1,
			slidesToShow: 3,
			loop: true,
			infinite: true,
			autoplay: false,
			autoplaySpeed: 3000,
    }

		// Initialize all div with carousel class
    var carousels = bulmaCarousel.attach('.carousel', options);

    // Loop on each carousel initialized
    for(var i = 0; i < carousels.length; i++) {
    	// Add listener to  event
    	carousels[i].on('before:show', state => {
    		console.log(state);
    	});
    }

    // Access to bulmaCarousel instance of an element
    var element = document.querySelector('#my-element');
    if (element && element.bulmaCarousel) {
    	// bulmaCarousel instance is available as element.bulmaCarousel
    	element.bulmaCarousel.on('before-show', function(state) {
    		console.log(state);
    	});
    }

    /*var player = document.getElementById('interpolation-video');
    player.addEventListener('loadedmetadata', function() {
      $('#interpolation-slider').on('input', function(event) {
        console.log(this.value, player.duration);
        player.currentTime = player.duration / 100 * this.value;
      })
    }, false);*/
    // preloadInterpolationImages();

    // $('#interpolation-slider').on('input', function(event) {
    //   setInterpolationImage(this.value);
    // });
    // setInterpolationImage(0);
    // $('#interpolation-slider').prop('max', NUM_INTERP_FRAMES - 1);

    bulmaSlider.attach();

})

// Function to toggle abstract expansion
function toggleAbstract() {
    const abstractFull = document.getElementById('abstractFull');
    const toggleButton = document.querySelector('.abstract-toggle');
    const toggleText = document.querySelector('.toggle-text');
    const toggleIcon = document.querySelector('.toggle-icon');
    
    if (abstractFull.classList.contains('expanded')) {
        // Collapse
        abstractFull.classList.remove('expanded');
        toggleButton.classList.remove('expanded');
        toggleText.textContent = 'Click to Read More';
    } else {
        // Expand
        abstractFull.classList.add('expanded');
        toggleButton.classList.add('expanded');
        toggleText.textContent = 'Click to Read Less';
    }
}

// =================================
// NAVIGATION SYSTEM FUNCTIONALITY
// =================================

class NavigationManager {
    constructor() {
        this.sections = ['introduction', 'data-collection', 'results', 'evaluation', 'citation'];
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
