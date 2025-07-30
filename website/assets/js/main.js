/**
 * Main JavaScript file for Clinical Skill-Mix Dimensions website
 * Handles navigation, interactions, and general UI functionality
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize explorer
    initializeExplorer();
    
    // Initialize info tabs
    initializeInfoTabs();
    
    // Load default dimension
    loadDimension('task-skills');
    
    console.log('Clinical Skill-Mix Dimensions app initialized');
}

/**
 * Navigation functionality
 */
function initializeNavigation() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
            updateActiveNavLink(this);
        });
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', updateNavOnScroll);
}

/**
 * Update active navigation link
 */
function updateActiveNavLink(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

/**
 * Update navigation based on scroll position
 */
function updateNavOnScroll() {
    const sections = ['overview', 'dimensions', 'explorer', 'about'];
    const scrollPosition = window.scrollY + 100;
    
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                const navLink = document.querySelector(`a[href="#${sectionId}"]`);
                if (navLink && !navLink.classList.contains('active')) {
                    updateActiveNavLink(navLink);
                }
            }
        }
    });
}

/**
 * Smooth scroll to section
 */
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const navHeight = document.querySelector('.navbar').offsetHeight;
        const targetPosition = section.offsetTop - navHeight;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
}

/**
 * Initialize explorer functionality
 */
function initializeExplorer() {
    // Dimension selector buttons
    const selectorButtons = document.querySelectorAll('.selector-btn');
    selectorButtons.forEach(button => {
        button.addEventListener('click', function() {
            const dimension = this.getAttribute('data-dimension');
            selectDimension(dimension, this);
        });
    });
    
    // View mode radio buttons
    const viewModeInputs = document.querySelectorAll('input[name="view-mode"]');
    viewModeInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.checked) {
                changeViewMode(this.value);
            }
        });
    });
    
    // Control checkboxes
    const showMetadata = document.getElementById('show-metadata');
    const showReferences = document.getElementById('show-references');
    
    if (showMetadata) {
        showMetadata.addEventListener('change', function() {
            toggleMetadata(this.checked);
        });
    }
    
    if (showReferences) {
        showReferences.addEventListener('change', function() {
            toggleReferences(this.checked);
        });
    }
}

/**
 * Select a dimension in the explorer
 */
function selectDimension(dimensionName, buttonElement) {
    // Update button states
    document.querySelectorAll('.selector-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    buttonElement.classList.add('active');
    
    // Update title
    const title = document.getElementById('current-dimension-title');
    if (title) {
        title.textContent = getDimensionDisplayName(dimensionName);
    }
    
    // Load dimension data
    loadDimension(dimensionName);
}

/**
 * Get display name for dimension
 */
function getDimensionDisplayName(dimensionName) {
    const displayNames = {
        'task-skills': 'Task Skills',
        'personas': 'Personas',
        'diseases': 'Diseases',
        'timeline': 'Timeline',
        'location-resources': 'Location-Resources'
    };
    return displayNames[dimensionName] || dimensionName;
}

/**
 * Change visualization view mode
 */
function changeViewMode(mode) {
    console.log('Changing view mode to:', mode);
    // This will be implemented when visualization is loaded
    const event = new CustomEvent('viewModeChanged', { detail: { mode } });
    document.dispatchEvent(event);
}

/**
 * Toggle metadata display
 */
function toggleMetadata(show) {
    console.log('Toggle metadata:', show);
    const event = new CustomEvent('metadataToggled', { detail: { show } });
    document.dispatchEvent(event);
}

/**
 * Toggle references display
 */
function toggleReferences(show) {
    console.log('Toggle references:', show);
    const event = new CustomEvent('referencesToggled', { detail: { show } });
    document.dispatchEvent(event);
}

/**
 * Initialize info tabs
 */
function initializeInfoTabs() {
    const tabButtons = document.querySelectorAll('.info-tab');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchInfoTab(tabName, this);
        });
    });
}

/**
 * Switch info tab
 */
function switchInfoTab(tabName, buttonElement) {
    // Update button states
    document.querySelectorAll('.info-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    buttonElement.classList.add('active');
    
    // Update panel visibility
    document.querySelectorAll('.info-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    
    const targetPanel = document.getElementById(`info-${tabName}`);
    if (targetPanel) {
        targetPanel.classList.add('active');
    }
}

/**
 * Export dimension data
 */
function exportDimension() {
    const currentDimension = getCurrentDimension();
    if (currentDimension) {
        console.log('Exporting dimension:', currentDimension);
        // Implementation will be added when dimension data is loaded
        alert('Export functionality will be implemented when dimension data is loaded');
    }
}

/**
 * Toggle fullscreen visualization
 */
function fullscreenVisualization() {
    const visualizationContainer = document.querySelector('.visualization-container');
    if (visualizationContainer) {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            visualizationContainer.requestFullscreen().catch(err => {
                console.log('Error attempting to enable fullscreen:', err);
            });
        }
    }
}

/**
 * Get current selected dimension
 */
function getCurrentDimension() {
    const activeButton = document.querySelector('.selector-btn.active');
    return activeButton ? activeButton.getAttribute('data-dimension') : null;
}

/**
 * Utility function to format numbers
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

/**
 * Utility function to capitalize words
 */
function capitalizeWords(str) {
    return str.replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Utility function to create HTML elements
 */
function createElement(tag, className = '', content = '') {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (content) element.textContent = content;
    return element;
}

/**
 * Utility function to show loading state
 */
function showLoading(container) {
    container.innerHTML = `
        <div class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading dimension data...</p>
        </div>
    `;
}

/**
 * Utility function to show error state
 */
function showError(container, message = 'An error occurred') {
    container.innerHTML = `
        <div class="error-state">
            <div class="error-icon">⚠️</div>
            <p>${message}</p>
            <button class="btn btn-outline" onclick="location.reload()">
                Retry
            </button>
        </div>
    `;
}

/**
 * Handle dimension card clicks
 */
document.addEventListener('click', function(e) {
    const dimensionCard = e.target.closest('.dimension-card');
    if (dimensionCard) {
        const dimension = dimensionCard.getAttribute('data-dimension');
        if (dimension) {
            // Scroll to explorer section
            scrollToSection('explorer');
            
            // Select the dimension after a brief delay to allow scrolling
            setTimeout(() => {
                const selectorButton = document.querySelector(`[data-dimension="${dimension}"]`);
                if (selectorButton) {
                    selectDimension(dimension, selectorButton);
                }
            }, 500);
        }
    }
});

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + 1-5 to switch dimensions
    if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '5') {
        e.preventDefault();
        const dimensions = ['task-skills', 'personas', 'diseases', 'timeline', 'location-resources'];
        const index = parseInt(e.key) - 1;
        if (dimensions[index]) {
            const button = document.querySelector(`[data-dimension="${dimensions[index]}"]`);
            if (button) {
                selectDimension(dimensions[index], button);
            }
        }
    }
    
    // Escape to exit fullscreen
    if (e.key === 'Escape' && document.fullscreenElement) {
        document.exitFullscreen();
    }
});

/**
 * Update UI based on data loading state
 */
function updateLoadingState(isLoading, dimension = null) {
    const visualizationContainer = document.getElementById('dimension-visualization');
    
    if (isLoading) {
        showLoading(visualizationContainer);
    } else if (dimension) {
        // This will be handled by the dimension loader
        console.log('Data loaded for dimension:', dimension);
    }
}

// Export functions for use by other modules
window.Clinical = {
    scrollToSection,
    loadDimension,
    updateLoadingState,
    getCurrentDimension,
    formatNumber,
    capitalizeWords,
    createElement,
    showLoading,
    showError
};