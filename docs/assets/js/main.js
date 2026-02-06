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
    loadDimension('care_task');

    console.log('Clinical World Model (8-dimension) app initialized');
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
    console.log('Initializing Cube Explorer (8-dimension framework: 5C + 3A)...');

    // Clinical Competency Space (5C) dimensions
    const dimensions5C = [
        { key: 'condition', file: 'conditions' },
        { key: 'care_phase', file: 'care_phases' },
        { key: 'care_setting', file: 'care_settings' },
        { key: 'care_task', file: 'care_task' },
        { key: 'care_provider_role', file: 'care_provider_role' }
    ];

    // AI Cognitive Engagement (3A) dimensions
    const dimensions3A = [
        { key: 'agent_facing', file: 'agent_facing' },
        { key: 'anchoring_layer', file: 'anchoring_layer' },
        { key: 'assigned_authority', file: 'assigned_authority' }
    ];

    // Load all dimensions
    const allDimensions = [...dimensions5C, ...dimensions3A];

    for (const dimension of allDimensions) {
        try {
            const response = await fetch(`clinical-skill-mix/${dimension.file}.json`);
            if (response.ok) {
                const data = await response.json();
                cubeExplorerData[dimension.key] = data.items || [];
                populateDropdown(dimension.key, data.items);
            } else {
                console.error(`Failed to load ${dimension.file}.json: ${response.status}`);
            }
        } catch (error) {
            console.error(`Error loading ${dimension.file}:`, error);
        }
    }

    // Add change listeners to all dropdowns
    allDimensions.forEach(dimension => {
        const selectId = dimension.key.replace(/_/g, '-') + '-select';
        const select = document.getElementById(selectId);
        if (select) {
            select.addEventListener('change', () => updateScenario(dimension.key, select.value));
        } else {
            console.warn(`Select element not found: ${selectId}`);
        }
    });

    console.log('Cube Explorer initialized with 8 dimensions');
}

/**
 * Populate dropdown with dimension items
 */
function populateDropdown(dimension, items) {
    const selectId = dimension.replace(/_/g, '-') + '-select';
    const select = document.getElementById(selectId);
    if (!select) {
        console.warn(`Select element not found: ${selectId}`);
        return;
    }

    // Dimension label mapping
    const dimensionLabels = {
        'condition': 'condition',
        'care_phase': 'care phase',
        'care_setting': 'care setting',
        'care_task': 'care task',
        'care_provider_role': 'provider role',
        'agent_facing': 'agent facing',
        'anchoring_layer': 'anchoring layer',
        'assigned_authority': 'assigned authority'
    };

    const label = dimensionLabels[dimension] || dimension;

    // Clear existing options except the first one
    select.innerHTML = `<option value="">Select a ${label}...</option>`;

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

    // Set default values after populating (use requestAnimationFrame to ensure DOM is updated)
    requestAnimationFrame(() => {
        setDefaultSelection(dimension, select);
    });
}

/**
 * Set default selection for a dimension
 */
function setDefaultSelection(dimension, select) {
    const defaults = {
        // Clinical Competency Space (5C)
        'condition': 'chapter-i/i25',  // ICD-10-CM I25: Chronic ischemic heart disease
        'care_phase': 'treatment-planning',
        'care_setting': 'emergency-room',
        'care_task': 'patient-care/patient-counseling',
        'care_provider_role': 'specialist-medical-practitioners/cardiology',

        // AI Cognitive Engagement (3A)
        'agent_facing': 'provider_facing',
        'anchoring_layer': 'input',
        'assigned_authority': 'augmentation'
    };

    const defaultValue = defaults[dimension];
    if (defaultValue) {
        console.log(`Setting default for ${dimension} to ${defaultValue}`);
        // Check if the option exists
        const option = select.querySelector(`option[value="${defaultValue}"]`);
        if (option) {
            console.log(`Option found for ${dimension}, setting value`);
            select.value = defaultValue;
            // Trigger the update immediately
            updateScenario(dimension, defaultValue);
        } else {
            console.warn(`Option not found for ${dimension} with value ${defaultValue}`);
            console.log(`Available options:`, Array.from(select.options).map(o => o.value));
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
 * Update the scenario text display (Combined 5C × 3A)
 */
function updateScenarioText() {
    const scenarioDiv = document.getElementById('combined-scenario');
    if (!scenarioDiv) {
        console.warn('Combined scenario div not found');
        return;
    }

    // Check if all 5C dimensions are selected
    const all5C = selectedScenario.condition &&
                  selectedScenario.care_phase &&
                  selectedScenario.care_setting &&
                  selectedScenario.care_task &&
                  selectedScenario.care_provider_role;

    // Check if all 3A dimensions are selected
    const all3A = selectedScenario.agent_facing &&
                  selectedScenario.anchoring_layer &&
                  selectedScenario.assigned_authority;

    // If not all dimensions selected, show prompt
    if (!all5C || !all3A) {
        scenarioDiv.className = 'scenario-text';
        scenarioDiv.innerHTML = 'Select dimensions from both cubes above to generate a complete Clinical Intelligence specification...';
        return;
    }

    // Helper function to convert role names to person forms
    function convertToPersonForm(name) {
        const conversions = {
            // Medical specialties
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
            'General Surgery': 'general surgeons',
            'Neurological Surgery': 'neurosurgeons',
            'Paediatric Surgery': 'pediatric surgeons',
            'Plastic Surgery': 'plastic surgeons',
            'Thoracic Surgery': 'thoracic surgeons',
            'Vascular Surgery': 'vascular surgeons',
            'Orthopaedics': 'orthopedic surgeons',
            'Internal Medicine': 'internists',
            'Respiratory Medicine': 'pulmonologists',
            'Forensic Medicine': 'forensic pathologists',
            'Occupational Medicine': 'occupational medicine physicians',
            'Rehabilitative Medicine': 'physiatrists',
            'Accident And Emergency Medicine': 'emergency medicine physicians',
            'Infectious Disease': 'infectious disease specialists',
            'Intensive Care': 'intensivists',
            'Child Psychiatrist': 'child psychiatrists',
            'Psychiatrist': 'psychiatrists',
            'Gerontopsychiatrist': 'gerontopsychiatrists',
            'Neuropsychiatrist': 'neuropsychiatrists',
            'Gynaecologist': 'gynaecologists',
            'Obstetrician': 'obstetricians',
            'Neonatologist': 'neonatologists',
            'Paediatrician': 'pediatricians',

            // General roles
            'Generalist Medical Practitioners': 'generalist medical practitioners',
            'Specialist Medical Practitioners': 'specialist medical practitioners',
            'Nursing Professionals': 'nursing professionals',
            'Midwifery Professionals': 'midwifery professionals',
            'Paramedical Practitioners': 'paramedical practitioners'
        };

        return conversions[name] || name.toLowerCase();
    }

    // Extract 5C values
    const providerRole = convertToPersonForm(selectedScenario.care_provider_role.name);
    const providerRoleSingular = providerRole.replace(/s$/, ''); // Remove trailing 's' for singular
    const careTask = selectedScenario.care_task.name.toLowerCase();
    const condition = selectedScenario.condition.name.toLowerCase();
    const carePhase = selectedScenario.care_phase.name.toLowerCase();
    const careSetting = selectedScenario.care_setting.name.toLowerCase();

    // Extract 3A values
    const agentFacingId = selectedScenario.agent_facing.id;
    const agentFacing = selectedScenario.agent_facing.name;
    const anchoringLayer = selectedScenario.anchoring_layer.name.toLowerCase();
    const assignedAuthority = selectedScenario.assigned_authority.name.toLowerCase();

    // Determine agent context based on agent-facing selection
    let agentContext = '';
    let agentPossessive = '';
    if (agentFacingId === 'provider_facing') {
        agentContext = providerRole;  // Just the role (plural: cardiologists)
        agentPossessive = providerRole + "'";  // cardiologists' (plural possessive)
    } else if (agentFacingId === 'encounter_facing') {
        agentContext = `${providerRoleSingular}-patient encounter`;
        agentPossessive = `${providerRoleSingular}-patient encounter's`;
    } else if (agentFacingId === 'patient_facing') {
        agentContext = `patient in ${providerRoleSingular}-patient care`;
        agentPossessive = `patient's in ${providerRoleSingular}-patient care`;
    } else {
        agentContext = providerRole;
        agentPossessive = providerRole + "'";
    }

    // Convert authority to verb form
    let authorityVerb = assignedAuthority;
    if (assignedAuthority === 'augmentation') {
        authorityVerb = 'augment';
    } else if (assignedAuthority === 'monitoring') {
        authorityVerb = 'monitor';
    } else if (assignedAuthority === 'automation') {
        authorityVerb = 'automate';
    }

    // Build unified single-sentence specification with correct grammar
    const scenarioHTML = `
        <div class="unified-specification">
            <p class="ai-competency-statement">
                AI Competency to
                <span class="dim-authority" style="color: var(--color-assigned-authority); font-weight: 700;">${authorityVerb}</span>
                <span class="dim-agent" style="color: var(--color-care-provider-role); font-weight: 700;">${agentPossessive}</span>
                <span class="dim-layer" style="color: var(--color-anchoring-layer); font-weight: 700;">${anchoringLayer} layer</span>
                for <span class="dim-task" style="color: var(--color-care-task); font-weight: 700;">${careTask}</span>
                in <span class="dim-condition" style="color: var(--color-condition); font-weight: 700;">${condition}</span>
                during <span class="dim-phase" style="color: var(--color-care-phase); font-weight: 700;">${carePhase}</span>
                within the <span class="dim-setting" style="color: var(--color-care-setting); font-weight: 700;">${careSetting}</span>.
            </p>
        </div>
    `;

    scenarioDiv.className = 'scenario-text populated';
    scenarioDiv.innerHTML = scenarioHTML;

    // Reinitialize Lucide icons for the new content
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

/**
 * Copy scenario text to clipboard
 */
function copyScenarioText() {
    const scenarioDiv = document.getElementById('combined-scenario');
    if (!scenarioDiv) {
        console.warn('Combined scenario div not found');
        return;
    }

    // Get text content without HTML
    const text = scenarioDiv.innerText || scenarioDiv.textContent;

    // Check if scenario is populated
    if (text.includes('Select dimensions')) {
        alert('Please select all dimensions from both cubes first to generate a specification.');
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


// ═══ BibTeX Copy ═══
function copyBibtex() {
    const bibtex = document.getElementById('bibtex-data').content.textContent.trim();
    const btn = document.querySelector('.bibtex-copy-btn');
    const label = btn.querySelector('.bibtex-btn-label');
    const icon = btn.querySelector('[data-lucide]');

    navigator.clipboard.writeText(bibtex).then(() => {
        label.textContent = 'Copied!';
        icon.setAttribute('data-lucide', 'check');
        btn.classList.add('bibtex-copied');
        if (window.lucide) lucide.createIcons();

        setTimeout(() => {
            label.textContent = 'Copy BibTeX';
            icon.setAttribute('data-lucide', 'clipboard-copy');
            btn.classList.remove('bibtex-copied');
            if (window.lucide) lucide.createIcons();
        }, 2000);
    }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = bibtex;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        label.textContent = 'Copied!';
        btn.classList.add('bibtex-copied');
        setTimeout(() => {
            label.textContent = 'Copy BibTeX';
            btn.classList.remove('bibtex-copied');
        }, 2000);
    });
}