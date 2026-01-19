/**
 * Dimension Loader - Handles loading and parsing dimension data
 * Fetches JSON files and processes them for visualization
 */

// Cache for loaded dimensions
const dimensionCache = new Map();

// Current dimension data
let currentDimensionData = null;

/**
 * Load dimension data from JSON file
 */
async function loadDimension(dimensionName) {
    try {
        // Show loading state
        updateLoadingState(true);
        
        // Check cache first
        if (dimensionCache.has(dimensionName)) {
            const cachedData = dimensionCache.get(dimensionName);
            currentDimensionData = cachedData;
            displayDimension(cachedData);
            updateLoadingState(false, dimensionName);
            return cachedData;
        }
        
        // Fetch dimension data
        const response = await fetch(`clinical-skill-mix/${dimensionName}.json`);
        
        if (!response.ok) {
            throw new Error(`Failed to load ${dimensionName}: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Process and validate data
        const processedData = processDimensionData(data);
        
        // Cache the data
        dimensionCache.set(dimensionName, processedData);
        currentDimensionData = processedData;
        
        // Display the dimension
        displayDimension(processedData);
        
        // Update info panels
        updateInfoPanels(processedData);
        
        updateLoadingState(false, dimensionName);
        
        console.log(`Loaded dimension: ${dimensionName}`, processedData);
        return processedData;
        
    } catch (error) {
        console.error('Error loading dimension:', error);
        
        const visualizationContainer = document.getElementById('dimension-visualization');
        showError(visualizationContainer, `Failed to load ${dimensionName} dimension: ${error.message}`);
        
        updateLoadingState(false);
        return null;
    }
}

/**
 * Process raw dimension data
 */
function processDimensionData(rawData) {
    const processedData = {
        ...rawData,
        statistics: calculateDimensionStatistics(rawData),
        hierarchyMap: buildHierarchyMap(rawData.items),
        maxDepth: Math.max(...rawData.items.map(item => item.depth))
    };
    
    return processedData;
}

/**
 * Calculate dimension statistics
 */
function calculateDimensionStatistics(data) {
    const items = data.items || [];
    
    const stats = {
        totalItems: items.length,
        itemsByDepth: {},
        averageChildrenPerParent: 0,
        maxChildren: 0,
        leafNodes: 0
    };
    
    // Count items by depth
    items.forEach(item => {
        const depth = item.depth;
        stats.itemsByDepth[depth] = (stats.itemsByDepth[depth] || 0) + 1;
        
        // Count leaf nodes (items with no children)
        if (!item.children_ids || item.children_ids.length === 0) {
            stats.leafNodes++;
        }
        
        // Track max children
        if (item.children_ids) {
            stats.maxChildren = Math.max(stats.maxChildren, item.children_ids.length);
        }
    });
    
    // Calculate average children per parent
    const parents = items.filter(item => item.children_ids && item.children_ids.length > 0);
    if (parents.length > 0) {
        const totalChildren = parents.reduce((sum, parent) => sum + parent.children_ids.length, 0);
        stats.averageChildrenPerParent = (totalChildren / parents.length).toFixed(1);
    }
    
    return stats;
}

/**
 * Build hierarchy map for quick lookups
 */
function buildHierarchyMap(items) {
    const hierarchyMap = {
        byId: new Map(),
        byDepth: new Map(),
        parents: new Map(),
        children: new Map()
    };
    
    // Index by ID
    items.forEach(item => {
        hierarchyMap.byId.set(item.id, item);
        
        // Index by depth
        if (!hierarchyMap.byDepth.has(item.depth)) {
            hierarchyMap.byDepth.set(item.depth, []);
        }
        hierarchyMap.byDepth.get(item.depth).push(item);
        
        // Index parent-child relationships
        if (item.parent_id) {
            hierarchyMap.parents.set(item.id, item.parent_id);
        }
        
        if (item.children_ids && item.children_ids.length > 0) {
            hierarchyMap.children.set(item.id, item.children_ids);
        }
    });
    
    return hierarchyMap;
}

/**
 * Display dimension data in the visualization area
 */
function displayDimension(data) {
    const container = document.getElementById('dimension-visualization');
    const viewMode = getSelectedViewMode();
    
    // Clear container
    container.innerHTML = '';
    
    // Render based on view mode
    switch (viewMode) {
        case 'hierarchy':
            renderHierarchicalView(container, data);
            break;
        case 'list':
            renderListView(container, data);
            break;
        case 'network':
            renderNetworkView(container, data);
            break;
        default:
            renderHierarchicalView(container, data);
    }
}

/**
 * Get selected view mode
 */
function getSelectedViewMode() {
    const checkedInput = document.querySelector('input[name="view-mode"]:checked');
    return checkedInput ? checkedInput.value : 'hierarchy';
}

/**
 * Render hierarchical view
 */
function renderHierarchicalView(container, data) {
    const hierarchyDiv = createElement('div', 'hierarchy-view');
    hierarchyDiv.setAttribute('data-dimension', data.dimension);

    // Create header
    const header = createElement('div', 'hierarchy-header');
    const frameworkInfo = data.reference && data.reference.classification ?
        `<span class="stat-chip framework-chip">Grounded Framework: ${data.reference.classification}</span>` : '';
    header.innerHTML = `
        <h4>${data.description}</h4>
        <div class="hierarchy-stats">
            <span class="stat-chip">Items: ${data.statistics.totalItems}</span>
            <span class="stat-chip">Max Depth: ${data.maxDepth}</span>
            <span class="stat-chip">Leaf Nodes: ${data.statistics.leafNodes}</span>
            ${frameworkInfo}
        </div>
    `;
    hierarchyDiv.appendChild(header);
    
    // Create tree structure
    const treeContainer = createElement('div', 'tree-container');
    const rootItems = data.items.filter(item => item.depth === 0);
    
    rootItems.forEach(rootItem => {
        const treeNode = createTreeNode(rootItem, data);
        treeContainer.appendChild(treeNode);
    });
    
    hierarchyDiv.appendChild(treeContainer);
    container.appendChild(hierarchyDiv);
}

/**
 * Create tree node for hierarchical view
 */
function createTreeNode(item, data) {
    const nodeDiv = createElement('div', `tree-node depth-${item.depth}`);
    
    // Node header
    const nodeHeader = createElement('div', 'node-header');
    const hasChildren = item.children_ids && item.children_ids.length > 0;
    
    nodeHeader.innerHTML = `
        <div class="node-toggle ${hasChildren ? 'expandable' : 'leaf'}">
            ${hasChildren ? '▶' : '•'}
        </div>
        <div class="node-icon">
            ${getNodeIcon(item, data.dimension)}
        </div>
        <div class="node-content">
            <div class="node-title">${item.name}</div>
            <div class="node-description">${item.description || ''}</div>
            ${shouldShowMetadata() ? createMetadataHTML(item) : ''}
        </div>
        <div class="node-badge">
            ${hasChildren ? item.children_ids.length : ''}
        </div>
    `;
    
    nodeDiv.appendChild(nodeHeader);
    
    // Children container
    if (hasChildren) {
        const childrenContainer = createElement('div', 'node-children collapsed');
        
        item.children_ids.forEach(childId => {
            const childItem = data.hierarchyMap.byId.get(childId);
            if (childItem) {
                const childNode = createTreeNode(childItem, data);
                childrenContainer.appendChild(childNode);
            }
        });
        
        nodeDiv.appendChild(childrenContainer);
        
        // Add click handler for expansion
        nodeHeader.addEventListener('click', function() {
            toggleNodeExpansion(nodeDiv, childrenContainer);
        });
    }
    
    return nodeDiv;
}

/**
 * Toggle node expansion
 */
function toggleNodeExpansion(nodeDiv, childrenContainer) {
    const toggle = nodeDiv.querySelector('.node-toggle');
    const isExpanded = !childrenContainer.classList.contains('collapsed');
    
    if (isExpanded) {
        childrenContainer.classList.add('collapsed');
        toggle.textContent = '▶';
        toggle.classList.remove('expanded');
    } else {
        childrenContainer.classList.remove('collapsed');
        toggle.textContent = '▼';
        toggle.classList.add('expanded');
    }
}

/**
 * Get icon for node based on dimension and item type
 */
function getNodeIcon(item, dimension) {
    const icons = {
        'task': {
            0: '🎯', // domains
            1: '⚡'  // competencies
        },
        'persona': {
            0: '👤', // roles
            1: '📋'  // specialties
        },
        'disease': {
            0: '📚', // chapters
            1: '🔬'  // conditions
        },
        'stage': {
            0: '⏰', // stages
            1: '➡️'  // transitions
        },
        'location': {
            0: '🏥', // locations
            1: '⚙️'  // resource levels
        }
    };
    
    return icons[dimension]?.[item.depth] || '📄';
}

/**
 * Create metadata HTML
 */
function createMetadataHTML(item) {
    if (!item.metadata || Object.keys(item.metadata).length === 0) {
        return '';
    }
    
    const metadataEntries = Object.entries(item.metadata)
        .slice(0, 3) // Show first 3 metadata items
        .map(([key, value]) => {
            const displayValue = Array.isArray(value) ? value.join(', ') : value;
            return `<span class="metadata-item"><strong>${formatMetadataKey(key)}:</strong> ${displayValue}</span>`;
        })
        .join('');
    
    return `<div class="node-metadata">${metadataEntries}</div>`;
}

/**
 * Format metadata key for display
 */
function formatMetadataKey(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Check if metadata should be shown
 */
function shouldShowMetadata() {
    const checkbox = document.getElementById('show-metadata');
    return checkbox ? checkbox.checked : true;
}

/**
 * Check if references should be shown
 */
function shouldShowReferences() {
    const checkbox = document.getElementById('show-references');
    return checkbox ? checkbox.checked : false;
}

/**
 * Render list view
 */
function renderListView(container, data) {
    const listDiv = createElement('div', 'list-view');
    listDiv.setAttribute('data-dimension', data.dimension);

    // Create header
    const header = createElement('div', 'list-header');
    header.innerHTML = `
        <h4>${data.description}</h4>
        <div class="list-controls">
            <input type="search" placeholder="Search items..." class="search-input">
            <select class="depth-filter">
                <option value="all">All Depths</option>
                ${Array.from(new Set(data.items.map(item => item.depth)))
                    .sort((a, b) => a - b)
                    .map(depth => `<option value="${depth}">Depth ${depth}</option>`)
                    .join('')}
            </select>
        </div>
    `;
    listDiv.appendChild(header);
    
    // Create list container
    const listContainer = createElement('div', 'list-container');
    
    // Sort items by depth, then by name
    const sortedItems = [...data.items].sort((a, b) => {
        if (a.depth !== b.depth) return a.depth - b.depth;
        return a.name.localeCompare(b.name);
    });
    
    sortedItems.forEach(item => {
        const listItem = createListItem(item, data);
        listContainer.appendChild(listItem);
    });
    
    listDiv.appendChild(listContainer);
    container.appendChild(listDiv);
    
    // Add search functionality
    const searchInput = header.querySelector('.search-input');
    const depthFilter = header.querySelector('.depth-filter');
    
    searchInput.addEventListener('input', () => filterListItems(searchInput.value, depthFilter.value, listContainer));
    depthFilter.addEventListener('change', () => filterListItems(searchInput.value, depthFilter.value, listContainer));
}

/**
 * Create list item
 */
function createListItem(item, data) {
    const listItem = createElement('div', `list-item depth-${item.depth}`);
    
    listItem.innerHTML = `
        <div class="list-item-icon">
            ${getNodeIcon(item, data.dimension)}
        </div>
        <div class="list-item-content">
            <div class="list-item-title">${item.name}</div>
            <div class="list-item-path">${item.path_components.join(' › ')}</div>
            <div class="list-item-description">${item.description || ''}</div>
            ${shouldShowMetadata() ? createMetadataHTML(item) : ''}
        </div>
        <div class="list-item-badge">
            <span class="depth-badge">D${item.depth}</span>
            ${item.children_ids && item.children_ids.length > 0 ? 
                `<span class="children-badge">${item.children_ids.length} children</span>` : 
                '<span class="leaf-badge">Leaf</span>'
            }
        </div>
    `;
    
    return listItem;
}

/**
 * Filter list items
 */
function filterListItems(searchTerm, depthFilter, container) {
    const items = container.querySelectorAll('.list-item');
    
    items.forEach(item => {
        const title = item.querySelector('.list-item-title').textContent.toLowerCase();
        const description = item.querySelector('.list-item-description').textContent.toLowerCase();
        const depthClass = Array.from(item.classList).find(cls => cls.startsWith('depth-'));
        const itemDepth = depthClass ? depthClass.replace('depth-', '') : '0';
        
        const matchesSearch = !searchTerm || 
            title.includes(searchTerm.toLowerCase()) || 
            description.includes(searchTerm.toLowerCase());
        
        const matchesDepth = depthFilter === 'all' || itemDepth === depthFilter;
        
        item.style.display = matchesSearch && matchesDepth ? 'flex' : 'none';
    });
}

/**
 * Render network view (simplified for now)
 */
function renderNetworkView(container, data) {
    const networkDiv = createElement('div', 'network-view');
    
    networkDiv.innerHTML = `
        <div class="network-placeholder">
            <div class="placeholder-icon">🔗</div>
            <h4>Network Visualization</h4>
            <p>Network view will show relationships between dimension items.</p>
            <p>This view is under development and will be available in a future update.</p>
            <div class="network-stats">
                <div class="stat">
                    <span class="stat-number">${data.statistics.totalItems}</span>
                    <span class="stat-label">Nodes</span>
                </div>
                <div class="stat">
                    <span class="stat-number">${data.items.filter(item => item.children_ids && item.children_ids.length > 0).length}</span>
                    <span class="stat-label">Edges</span>
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(networkDiv);
}

/**
 * Update info panels with dimension data
 */
function updateInfoPanels(data) {
    updateOverviewPanel(data);
    updateStatisticsPanel(data);
    updateReferencePanel(data);
}

/**
 * Update overview panel
 */
function updateOverviewPanel(data) {
    const panel = document.getElementById('info-overview');
    if (panel) {
        panel.innerHTML = `
            <h4>${getDimensionDisplayName(data.dimension)}</h4>
            <p>${data.description}</p>
            
            <div class="overview-metrics">
                <div class="metric-grid">
                    <div class="metric-card">
                        <span class="metric-number">${data.statistics.totalItems}</span>
                        <span class="metric-label">Total Items</span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-number">${data.maxDepth + 1}</span>
                        <span class="metric-label">Hierarchy Levels</span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-number">${data.statistics.leafNodes}</span>
                        <span class="metric-label">Leaf Nodes</span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-number">${data.statistics.averageChildrenPerParent}</span>
                        <span class="metric-label">Avg Children</span>
                    </div>
                </div>
            </div>
            
            <div class="hierarchy-breakdown">
                <h5>Hierarchy Breakdown</h5>
                ${Object.entries(data.statistics.itemsByDepth)
                    .map(([depth, count]) => `
                        <div class="depth-stat">
                            <span class="depth-label">Level ${depth} (${data.hierarchy.levels[depth] || 'Unknown'}):</span>
                            <span class="depth-count">${count} items</span>
                        </div>
                    `).join('')}
            </div>
        `;
    }
}

/**
 * Update statistics panel
 */
function updateStatisticsPanel(data) {
    const panel = document.getElementById('info-statistics');
    if (panel) {
        panel.innerHTML = `
            <h4>Statistical Analysis</h4>
            
            <div class="stats-section">
                <h5>Distribution</h5>
                <div class="distribution-chart">
                    ${Object.entries(data.statistics.itemsByDepth)
                        .map(([depth, count]) => {
                            const percentage = ((count / data.statistics.totalItems) * 100).toFixed(1);
                            return `
                                <div class="distribution-bar">
                                    <span class="bar-label">Level ${depth}</span>
                                    <div class="bar-container">
                                        <div class="bar-fill" style="width: ${percentage}%"></div>
                                    </div>
                                    <span class="bar-value">${count} (${percentage}%)</span>
                                </div>
                            `;
                        }).join('')}
                </div>
            </div>
            
            <div class="stats-section">
                <h5>Structural Metrics</h5>
                <div class="metrics-table">
                    <div class="metric-row">
                        <span class="metric-name">Total Items</span>
                        <span class="metric-value">${data.statistics.totalItems}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Maximum Depth</span>
                        <span class="metric-value">${data.maxDepth}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Leaf Nodes</span>
                        <span class="metric-value">${data.statistics.leafNodes}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Parent Nodes</span>
                        <span class="metric-value">${data.statistics.totalItems - data.statistics.leafNodes}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Max Children per Node</span>
                        <span class="metric-value">${data.statistics.maxChildren}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Avg Children per Parent</span>
                        <span class="metric-value">${data.statistics.averageChildrenPerParent}</span>
                    </div>
                </div>
            </div>
        `;
    }
}

/**
 * Update reference panel
 */
function updateReferencePanel(data) {
    const panel = document.getElementById('info-reference');
    if (panel) {
        const reference = data.reference || {};
        
        panel.innerHTML = `
            <h4>Evidence Base & References</h4>
            
            ${reference.classification ? `
                <div class="reference-section">
                    <h5>Classification System</h5>
                    <p>${reference.classification}</p>
                </div>
            ` : ''}
            
            ${reference.burden_metric ? `
                <div class="reference-section">
                    <h5>Burden Metric</h5>
                    <p>${reference.burden_metric}</p>
                </div>
            ` : ''}
            
            ${reference.data_source ? `
                <div class="reference-section">
                    <h5>Data Source</h5>
                    <p>${reference.data_source}</p>
                </div>
            ` : ''}
            
            ${reference.sources && reference.sources.length > 0 ? `
                <div class="reference-section">
                    <h5>Sources</h5>
                    <ul class="sources-list">
                        ${reference.sources.map(source => `<li>${source}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${reference.last_updated ? `
                <div class="reference-section">
                    <h5>Last Updated</h5>
                    <p class="last-updated">${reference.last_updated}</p>
                </div>
            ` : ''}
            
            ${data.dimension_metadata ? `
                <div class="reference-section">
                    <h5>Dimension Metadata</h5>
                    <div class="metadata-grid">
                        ${Object.entries(data.dimension_metadata)
                            .slice(0, 5) // Show first 5 metadata items
                            .map(([key, value]) => `
                                <div class="metadata-row">
                                    <span class="metadata-key">${formatMetadataKey(key)}</span>
                                    <span class="metadata-value">${typeof value === 'object' ? JSON.stringify(value, null, 2) : value}</span>
                                </div>
                            `).join('')}
                    </div>
                </div>
            ` : ''}
        `;
    }
}

// Listen for view mode and control changes
document.addEventListener('viewModeChanged', function(event) {
    if (currentDimensionData) {
        displayDimension(currentDimensionData);
    }
});

document.addEventListener('metadataToggled', function(event) {
    if (currentDimensionData) {
        displayDimension(currentDimensionData);
    }
});

document.addEventListener('referencesToggled', function(event) {
    if (currentDimensionData) {
        displayDimension(currentDimensionData);
    }
});

// Export functions
window.DimensionLoader = {
    loadDimension,
    getCurrentDimensionData: () => currentDimensionData,
    getDimensionCache: () => dimensionCache
};