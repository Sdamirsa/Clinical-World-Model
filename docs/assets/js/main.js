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

    // Initialize cube explorer
    initializeCubeExplorer();

    // Load default dimension
    loadDimension('task');

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
    const sections = ['introduction', 'framework', 'overview', 'cube-explorer', 'components', 'explorer', 'decision-making', 'about'];
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
        'task': 'Task',
        'persona': 'Persona',
        'disease': 'Disease',
        'stage': 'Stage',
        'location': 'Location'
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
        const dimensions = ['task', 'persona', 'disease', 'stage', 'location'];
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

/**
 * Initialize Cube Explorer
 */
let cubeExplorerData = {
    disease: [],
    stage: [],
    location: [],
    task: [],
    persona: []
};

let selectedScenario = {
    disease: null,
    stage: null,
    location: null,
    task: null,
    persona: null
};

async function initializeCubeExplorer() {
    console.log('Initializing Cube Explorer...');

    // Load all dimension data
    const dimensions = ['disease', 'stage', 'location', 'task', 'persona'];

    for (const dimension of dimensions) {
        try {
            const response = await fetch(`clinical-skill-mix/${dimension}.json`);
            if (response.ok) {
                const data = await response.json();
                cubeExplorerData[dimension] = data.items || [];
                populateDropdown(dimension, data.items);
            }
        } catch (error) {
            console.error(`Error loading ${dimension}:`, error);
        }
    }

    // Add change listeners to all dropdowns
    dimensions.forEach(dimension => {
        const select = document.getElementById(`${dimension}-select`);
        if (select) {
            select.addEventListener('change', () => updateScenario(dimension, select.value));
        }
    });

    console.log('Cube Explorer initialized');
}

/**
 * Populate dropdown with dimension items
 */
function populateDropdown(dimension, items) {
    const select = document.getElementById(`${dimension}-select`);
    if (!select) return;

    // Clear existing options except the first one
    select.innerHTML = '<option value="">Select a ' + dimension + '...</option>';

    // Show all items as a flat list
    const displayItems = items;

    // Sort items by name
    displayItems.sort((a, b) => a.name.localeCompare(b.name));

    // Add options
    displayItems.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.name;
        select.appendChild(option);
    });

    // Set default values after populating
    setDefaultSelection(dimension, select);
}

/**
 * Set default selection for a dimension
 */
function setDefaultSelection(dimension, select) {
    const defaults = {
        'disease': 'cardiovascular/ischaemic-heart-disease',
        'stage': 'treatment-planning',
        'location': 'emergency-room',
        'task': 'patient-care/patient-counseling',
        'persona': 'specialist-medical-practitioners/cardiology'
    };

    const defaultValue = defaults[dimension];
    if (defaultValue) {
        // Check if the option exists
        const option = select.querySelector(`option[value="${defaultValue}"]`);
        if (option) {
            select.value = defaultValue;
            // Trigger the update
            updateScenario(dimension, defaultValue);
        }
    }
}

/**
 * Update scenario when a dimension changes
 */
function updateScenario(dimension, itemId) {
    // Find the selected item
    const item = cubeExplorerData[dimension].find(i => i.id === itemId);
    selectedScenario[dimension] = item;

    // Update the scenario text
    updateScenarioText();
}

/**
 * Update the scenario text display
 */
function updateScenarioText() {
    const scenarioDiv = document.getElementById('scenario-text');
    if (!scenarioDiv) return;

    // Check if all dimensions are selected
    const allSelected = Object.values(selectedScenario).every(item => item !== null);

    if (!allSelected) {
        scenarioDiv.className = 'scenario-text';
        scenarioDiv.innerHTML = 'Select elements from each dimension above to generate a clinical competency...';
        return;
    }

    // Helper function to convert specialty names to person forms (plurals)
    function convertToPersonForm(name) {
        const conversions = {
            // -ology specialties
            'Cardiology': 'cardiologists',
            'Neurology': 'neurologists',
            'Radiology': 'radiologists',
            'Oncology': 'oncologists',
            'Urology': 'urologists',
            'Anaesthesiology': 'anesthesiologists',
            'Dermatovenerology': 'dermatovenereologists',
            'Gastroenterology': 'gastroenterologists',
            'Haematology': 'hematologists',
            'Immunology': 'immunologists',
            'Ophthalmology': 'ophthalmologists',
            'Otolaryngology': 'otolaryngologists',

            // Surgery specialties
            'General Surgery': 'general surgeons',
            'Neurological Surgery': 'neurosurgeons',
            'Paediatric Surgery': 'pediatric surgeons',
            'Plastic Surgery': 'plastic surgeons',
            'Thoracic Surgery': 'thoracic surgeons',
            'Vascular Surgery': 'vascular surgeons',
            'Orthopaedics': 'orthopedic surgeons',

            // Medicine specialties
            'Internal Medicine': 'internists',
            'Respiratory Medicine': 'pulmonologists',
            'Forensic Medicine': 'forensic pathologists',
            'Occupational Medicine': 'occupational medicine physicians',
            'Rehabilitative Medicine': 'physiatrists',
            'Accident And Emergency Medicine': 'emergency medicine physicians',

            // Other specialties
            'Infectious Disease': 'infectious disease specialists',
            'Intensive Care': 'intensivists',

            // Already in person form - just lowercase and pluralize if needed
            'Child Psychiatrist': 'child psychiatrists',
            'Psychiatrist': 'psychiatrists',
            'Gerontopsychiatrist': 'gerontopsychiatrists',
            'Neuropsychiatrist': 'neuropsychiatrists',
            'Gynaecologist': 'gynaecologists',
            'Obstetrician': 'obstetricians',
            'Neonatologist': 'neonatologists',
            'Paediatrician': 'pediatricians'
        };

        return conversions[name] || name.toLowerCase();
    }

    // Build the scenario text with unified flow
    const persona = convertToPersonForm(selectedScenario.persona.name);
    const task = selectedScenario.task.name.toLowerCase();
    const disease = selectedScenario.disease.name.toLowerCase();
    const stage = selectedScenario.stage.name.toLowerCase();
    const location = selectedScenario.location.name.toLowerCase();

    const scenarioText = `Intelligence system competency to augment <span class="dimension-value dimension-persona">${persona}</span> for <span class="dimension-value dimension-task">${task}</span> task in the care of <span class="dimension-value dimension-disease">${disease}</span> at the <span class="dimension-value dimension-stage">${stage}</span> stage in <span class="dimension-value dimension-location">${location}</span>`;

    scenarioDiv.className = 'scenario-text populated';
    scenarioDiv.innerHTML = scenarioText;
}

/**
 * Copy scenario text to clipboard
 */
function copyScenarioText() {
    const scenarioDiv = document.getElementById('scenario-text');
    if (!scenarioDiv) return;

    // Get text content without HTML
    const text = scenarioDiv.innerText || scenarioDiv.textContent;

    // Check if scenario is populated
    if (text.includes('Select elements')) {
        alert('Please select all dimensions first to generate a scenario.');
        return;
    }

    // Copy to clipboard
    navigator.clipboard.writeText(text).then(() => {
        // Show feedback
        const button = event.target.closest('button');
        if (button) {
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i data-lucide="check"></i> Copied!';
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            setTimeout(() => {
                button.innerHTML = originalHTML;
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }, 2000);
        }
    }).catch(err => {
        console.error('Failed to copy text:', err);
        alert('Failed to copy to clipboard');
    });
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

// Make copyScenarioText globally available
window.copyScenarioText = copyScenarioText;