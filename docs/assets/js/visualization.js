/**
 * Visualization utilities and enhanced styling for dimension display
 * Handles dynamic styling, animations, and interactive elements
 */

// Add dynamic styles for the dimension visualization
function addVisualizationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        /* Hierarchy View Styles */
        .hierarchy-view {
            padding: var(--spacing-4);
        }
        
        .hierarchy-header {
            margin-bottom: var(--spacing-6);
            padding-bottom: var(--spacing-4);
            border-bottom: 2px solid var(--gray-200);
        }
        
        .hierarchy-header h4 {
            margin-bottom: var(--spacing-2);
            color: var(--gray-900);
        }
        
        .hierarchy-stats {
            display: flex;
            gap: var(--spacing-3);
            flex-wrap: wrap;
        }
        
        .stat-chip {
            background: var(--primary-color);
            color: var(--white);
            padding: var(--spacing-1) var(--spacing-3);
            border-radius: var(--radius-full);
            font-size: var(--font-size-xs);
            font-weight: 500;
        }
        
        /* Tree Container */
        .tree-container {
            max-height: 600px;
            overflow-y: auto;
            padding-right: var(--spacing-2);
        }
        
        .tree-container::-webkit-scrollbar {
            width: 6px;
        }
        
        .tree-container::-webkit-scrollbar-track {
            background: var(--gray-100);
            border-radius: var(--radius-base);
        }
        
        .tree-container::-webkit-scrollbar-thumb {
            background: var(--gray-300);
            border-radius: var(--radius-base);
        }
        
        .tree-container::-webkit-scrollbar-thumb:hover {
            background: var(--gray-400);
        }
        
        /* Tree Node Styles */
        .tree-node {
            margin-bottom: var(--spacing-2);
            border-radius: var(--radius-lg);
            transition: all 0.2s ease;
        }
        
        .tree-node.depth-0 {
            background: var(--white);
            border: 2px solid var(--primary-color);
            box-shadow: var(--shadow-sm);
        }
        
        .tree-node.depth-1 {
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            margin-left: var(--spacing-6);
        }
        
        .tree-node.depth-2 {
            background: var(--white);
            border: 1px solid var(--gray-100);
            margin-left: var(--spacing-12);
        }
        
        .node-header {
            display: flex;
            align-items: flex-start;
            gap: var(--spacing-3);
            padding: var(--spacing-4);
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        
        .node-header:hover {
            background-color: rgba(37, 99, 235, 0.05);
        }
        
        .node-toggle {
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: var(--font-size-sm);
            color: var(--gray-500);
            transition: transform 0.2s ease;
            flex-shrink: 0;
        }
        
        .node-toggle.expandable {
            cursor: pointer;
            color: var(--primary-color);
        }
        
        .node-toggle.expanded {
            transform: rotate(90deg);
        }
        
        .node-toggle.leaf {
            color: var(--gray-300);
        }
        
        .node-icon {
            font-size: var(--font-size-lg);
            flex-shrink: 0;
        }
        
        .node-content {
            flex: 1;
            min-width: 0;
        }
        
        .node-title {
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: var(--spacing-1);
            font-size: var(--font-size-base);
        }
        
        .node-description {
            color: var(--gray-600);
            font-size: var(--font-size-sm);
            line-height: 1.4;
            margin-bottom: var(--spacing-2);
        }
        
        .node-metadata {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-1);
            margin-top: var(--spacing-2);
        }
        
        .metadata-item {
            font-size: var(--font-size-xs);
            color: var(--gray-500);
            padding: var(--spacing-1) var(--spacing-2);
            background: var(--gray-100);
            border-radius: var(--radius-base);
        }
        
        .metadata-item strong {
            color: var(--gray-700);
        }
        
        .node-badge {
            background: var(--accent-color);
            color: var(--white);
            padding: var(--spacing-1) var(--spacing-2);
            border-radius: var(--radius-base);
            font-size: var(--font-size-xs);
            font-weight: 500;
            min-width: 20px;
            text-align: center;
            flex-shrink: 0;
        }
        
        .node-children {
            padding-left: var(--spacing-4);
            border-left: 2px solid var(--gray-200);
            margin-left: var(--spacing-6);
            transition: all 0.3s ease;
            overflow: hidden;
        }
        
        .node-children.collapsed {
            max-height: 0;
            padding-top: 0;
            padding-bottom: 0;
            margin-bottom: 0;
        }
        
        .node-children:not(.collapsed) {
            max-height: 2000px;
            padding-top: var(--spacing-2);
            padding-bottom: var(--spacing-2);
        }
        
        /* List View Styles */
        .list-view {
            padding: var(--spacing-4);
        }
        
        .list-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-6);
            padding-bottom: var(--spacing-4);
            border-bottom: 2px solid var(--gray-200);
            flex-wrap: wrap;
            gap: var(--spacing-4);
        }
        
        .list-header h4 {
            margin: 0;
            color: var(--gray-900);
        }
        
        .list-controls {
            display: flex;
            gap: var(--spacing-3);
            align-items: center;
        }
        
        .search-input {
            padding: var(--spacing-2) var(--spacing-4);
            border: 1px solid var(--gray-300);
            border-radius: var(--radius-lg);
            font-size: var(--font-size-sm);
            min-width: 200px;
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        .depth-filter {
            padding: var(--spacing-2) var(--spacing-4);
            border: 1px solid var(--gray-300);
            border-radius: var(--radius-lg);
            font-size: var(--font-size-sm);
            background: var(--white);
        }
        
        .list-container {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-3);
            max-height: 600px;
            overflow-y: auto;
        }
        
        .list-item {
            display: flex;
            align-items: flex-start;
            gap: var(--spacing-4);
            padding: var(--spacing-4);
            background: var(--white);
            border: 1px solid var(--gray-200);
            border-radius: var(--radius-lg);
            transition: all 0.2s ease;
        }
        
        .list-item:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary-color);
        }
        
        .list-item.depth-0 {
            border-left: 4px solid var(--primary-color);
        }
        
        .list-item.depth-1 {
            border-left: 4px solid var(--accent-color);
        }
        
        .list-item.depth-2 {
            border-left: 4px solid var(--warning-color);
        }
        
        .list-item-icon {
            font-size: var(--font-size-xl);
            flex-shrink: 0;
        }
        
        .list-item-content {
            flex: 1;
            min-width: 0;
        }
        
        .list-item-title {
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: var(--spacing-1);
        }
        
        .list-item-path {
            font-size: var(--font-size-xs);
            color: var(--gray-500);
            margin-bottom: var(--spacing-2);
            font-family: monospace;
        }
        
        .list-item-description {
            color: var(--gray-600);
            font-size: var(--font-size-sm);
            line-height: 1.4;
        }
        
        .list-item-badge {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-1);
            align-items: flex-end;
            flex-shrink: 0;
        }
        
        .depth-badge {
            background: var(--gray-500);
            color: var(--white);
            padding: var(--spacing-1) var(--spacing-2);
            border-radius: var(--radius-base);
            font-size: var(--font-size-xs);
            font-weight: 500;
        }
        
        .children-badge {
            background: var(--accent-color);
            color: var(--white);
            padding: var(--spacing-1) var(--spacing-2);
            border-radius: var(--radius-base);
            font-size: var(--font-size-xs);
            font-weight: 500;
        }
        
        .leaf-badge {
            background: var(--gray-300);
            color: var(--gray-700);
            padding: var(--spacing-1) var(--spacing-2);
            border-radius: var(--radius-base);
            font-size: var(--font-size-xs);
            font-weight: 500;
        }
        
        /* Network View Styles */
        .network-view {
            padding: var(--spacing-8);
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .network-placeholder {
            text-align: center;
            color: var(--gray-500);
        }
        
        .placeholder-icon {
            font-size: 4rem;
            margin-bottom: var(--spacing-4);
        }
        
        .network-placeholder h4 {
            color: var(--gray-700);
            margin-bottom: var(--spacing-2);
        }
        
        .network-placeholder p {
            margin-bottom: var(--spacing-2);
        }
        
        .network-stats {
            display: flex;
            justify-content: center;
            gap: var(--spacing-8);
            margin-top: var(--spacing-6);
        }
        
        .network-stats .stat {
            text-align: center;
        }
        
        .network-stats .stat-number {
            display: block;
            font-size: var(--font-size-2xl);
            font-weight: 700;
            color: var(--primary-color);
        }
        
        .network-stats .stat-label {
            font-size: var(--font-size-sm);
            color: var(--gray-500);
        }
        
        /* Info Panel Styles */
        .overview-metrics {
            margin: var(--spacing-6) 0;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: var(--spacing-4);
            margin-bottom: var(--spacing-6);
        }
        
        .metric-card {
            background: var(--gray-50);
            padding: var(--spacing-4);
            border-radius: var(--radius-lg);
            text-align: center;
            border: 1px solid var(--gray-200);
        }
        
        .metric-number {
            display: block;
            font-size: var(--font-size-2xl);
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: var(--spacing-1);
        }
        
        .metric-label {
            font-size: var(--font-size-sm);
            color: var(--gray-600);
            font-weight: 500;
        }
        
        .hierarchy-breakdown {
            background: var(--white);
            padding: var(--spacing-4);
            border-radius: var(--radius-lg);
            border: 1px solid var(--gray-200);
        }
        
        .hierarchy-breakdown h5 {
            margin-bottom: var(--spacing-4);
            color: var(--gray-900);
        }
        
        .depth-stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-2) 0;
            border-bottom: 1px solid var(--gray-100);
        }
        
        .depth-stat:last-child {
            border-bottom: none;
        }
        
        .depth-label {
            color: var(--gray-700);
            font-weight: 500;
        }
        
        .depth-count {
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* Statistics Panel */
        .stats-section {
            margin-bottom: var(--spacing-6);
        }
        
        .stats-section h5 {
            margin-bottom: var(--spacing-4);
            color: var(--gray-900);
        }
        
        .distribution-chart {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-3);
        }
        
        .distribution-bar {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
        }
        
        .bar-label {
            min-width: 80px;
            font-size: var(--font-size-sm);
            color: var(--gray-600);
            font-weight: 500;
        }
        
        .bar-container {
            flex: 1;
            height: 20px;
            background: var(--gray-200);
            border-radius: var(--radius-base);
            overflow: hidden;
        }
        
        .bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
            transition: width 0.5s ease;
        }
        
        .bar-value {
            min-width: 100px;
            text-align: right;
            font-size: var(--font-size-sm);
            color: var(--gray-700);
            font-weight: 500;
        }
        
        .metrics-table {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-2);
        }
        
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-3);
            background: var(--gray-50);
            border-radius: var(--radius-base);
        }
        
        .metric-name {
            color: var(--gray-700);
            font-weight: 500;
        }
        
        .metric-value {
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* Reference Panel */
        .reference-section {
            margin-bottom: var(--spacing-6);
        }
        
        .reference-section h5 {
            margin-bottom: var(--spacing-3);
            color: var(--gray-900);
        }
        
        .reference-section p {
            color: var(--gray-600);
            line-height: 1.6;
        }
        
        .sources-list {
            list-style: none;
            padding: 0;
        }
        
        .sources-list li {
            padding: var(--spacing-2) 0;
            border-bottom: 1px solid var(--gray-100);
            color: var(--gray-600);
        }
        
        .sources-list li:last-child {
            border-bottom: none;
        }
        
        .last-updated {
            color: var(--gray-500);
            font-style: italic;
        }
        
        .metadata-grid {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-2);
        }
        
        .metadata-row {
            display: flex;
            gap: var(--spacing-3);
            padding: var(--spacing-2);
            background: var(--gray-50);
            border-radius: var(--radius-base);
        }
        
        .metadata-key {
            font-weight: 500;
            color: var(--gray-700);
            min-width: 120px;
        }
        
        .metadata-value {
            color: var(--gray-600);
            font-family: monospace;
            font-size: var(--font-size-sm);
            overflow-wrap: break-word;
        }
        
        /* Error States */
        .error-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 300px;
            color: var(--error-color);
            text-align: center;
        }
        
        .error-icon {
            font-size: 3rem;
            margin-bottom: var(--spacing-4);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .tree-node,
        .list-item {
            animation: fadeIn 0.3s ease forwards;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .metric-grid {
                grid-template-columns: 1fr;
            }
            
            .list-header {
                flex-direction: column;
                align-items: stretch;
            }
            
            .list-controls {
                flex-direction: column;
            }
            
            .search-input {
                min-width: auto;
            }
            
            .distribution-bar {
                flex-direction: column;
                gap: var(--spacing-1);
            }
            
            .bar-label,
            .bar-value {
                min-width: auto;
                text-align: left;
            }
            
            .metric-row {
                flex-direction: column;
                align-items: flex-start;
                gap: var(--spacing-1);
            }
            
            .metadata-row {
                flex-direction: column;
                gap: var(--spacing-1);
            }
            
            .metadata-key {
                min-width: auto;
            }
        }
    `;
    
    document.head.appendChild(style);
}

// Add search highlighting functionality
function highlightSearchTerms(container, searchTerm) {
    if (!searchTerm) return;
    
    const textNodes = [];
    const walker = document.createTreeWalker(
        container,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    let node;
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    
    textNodes.forEach(textNode => {
        const text = textNode.textContent;
        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        
        if (regex.test(text)) {
            const highlightedHTML = text.replace(regex, '<mark class="search-highlight">$1</mark>');
            const wrapper = document.createElement('span');
            wrapper.innerHTML = highlightedHTML;
            textNode.parentNode.replaceChild(wrapper, textNode);
        }
    });
}

// Escape special regex characters
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Add dynamic animations for tree expansion
function addTreeAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        .search-highlight {
            background-color: #fef08a;
            color: #92400e;
            padding: 1px 2px;
            border-radius: 2px;
        }
        
        .node-children {
            transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                       padding 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                       margin 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .tree-node:hover .node-header {
            background-color: rgba(37, 99, 235, 0.08);
        }
        
        .list-item {
            transform: translateX(0);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .list-item:hover {
            transform: translateX(4px) translateY(-1px);
        }
    `;
    
    document.head.appendChild(style);
}

// Initialize visualization enhancements
function initializeVisualizationEnhancements() {
    addVisualizationStyles();
    addTreeAnimations();
    
    // Add keyboard navigation for trees
    document.addEventListener('keydown', function(e) {
        if (e.target.closest('.tree-container')) {
            handleTreeKeyNavigation(e);
        }
    });
}

// Handle keyboard navigation in tree view
function handleTreeKeyNavigation(e) {
    const currentNode = document.activeElement.closest('.tree-node');
    if (!currentNode) return;
    
    let targetNode = null;
    
    switch (e.key) {
        case 'ArrowDown':
            targetNode = getNextTreeNode(currentNode);
            break;
        case 'ArrowUp':
            targetNode = getPreviousTreeNode(currentNode);
            break;
        case 'ArrowRight':
            expandTreeNode(currentNode);
            break;
        case 'ArrowLeft':
            collapseTreeNode(currentNode);
            break;
        case 'Enter':
        case ' ':
            toggleTreeNode(currentNode);
            e.preventDefault();
            break;
    }
    
    if (targetNode) {
        targetNode.querySelector('.node-header').focus();
        e.preventDefault();
    }
}

// Get next tree node for keyboard navigation
function getNextTreeNode(currentNode) {
    const allNodes = Array.from(document.querySelectorAll('.tree-node'));
    const currentIndex = allNodes.indexOf(currentNode);
    return allNodes[currentIndex + 1] || null;
}

// Get previous tree node for keyboard navigation  
function getPreviousTreeNode(currentNode) {
    const allNodes = Array.from(document.querySelectorAll('.tree-node'));
    const currentIndex = allNodes.indexOf(currentNode);
    return allNodes[currentIndex - 1] || null;
}

// Expand tree node
function expandTreeNode(node) {
    const childrenContainer = node.querySelector('.node-children');
    const toggle = node.querySelector('.node-toggle');
    
    if (childrenContainer && childrenContainer.classList.contains('collapsed')) {
        childrenContainer.classList.remove('collapsed');
        toggle.textContent = '▼';
        toggle.classList.add('expanded');
    }
}

// Collapse tree node
function collapseTreeNode(node) {
    const childrenContainer = node.querySelector('.node-children');
    const toggle = node.querySelector('.node-toggle');
    
    if (childrenContainer && !childrenContainer.classList.contains('collapsed')) {
        childrenContainer.classList.add('collapsed');
        toggle.textContent = '▶';
        toggle.classList.remove('expanded');
    }
}

// Toggle tree node
function toggleTreeNode(node) {
    const childrenContainer = node.querySelector('.node-children');
    
    if (childrenContainer) {
        if (childrenContainer.classList.contains('collapsed')) {
            expandTreeNode(node);
        } else {
            collapseTreeNode(node);
        }
    }
}

// Add export functionality
function addExportFunctionality() {
    window.exportDimension = function() {
        const currentData = window.DimensionLoader?.getCurrentDimensionData();
        if (!currentData) {
            alert('No dimension data loaded');
            return;
        }
        
        const dataStr = JSON.stringify(currentData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `${currentData.dimension}-dimension.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeVisualizationEnhancements();
    addExportFunctionality();
});

// Export utilities
window.VisualizationUtils = {
    highlightSearchTerms,
    addTreeAnimations,
    expandTreeNode,
    collapseTreeNode,
    toggleTreeNode
};