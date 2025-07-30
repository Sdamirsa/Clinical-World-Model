#!/usr/bin/env python3
"""
Pydantic models for Clinical Skill-Mix dimensions
Hierarchical path-based structure with flexible depth selection
"""

from datetime import date
from typing import List, Optional, Dict, Any, Union, Tuple
from pydantic import BaseModel, Field, validator
from enum import Enum
from itertools import product

# =============================================================================
# Enums and Constants
# =============================================================================

class DALYRankingCategory(str, Enum):
    """DALY burden ranking categories (simplified)"""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"

class ResourceLevel(str, Enum):
    """Resource availability levels (simplified)"""
    LIMITED = "limited"
    RICH = "rich"

class DimensionType(str, Enum):
    """Types of skill-mix dimensions"""
    TASK_SKILLS = "task-skills"
    PERSONAS = "personas"
    DISEASES = "diseases"
    TIMELINE = "timeline"
    LOCATION_RESOURCES = "location-resources"

# =============================================================================
# Base Models
# =============================================================================

class ReferenceInfo(BaseModel):
    """Standard reference information for evidence-based dimensions"""
    classification: Optional[str] = Field(None, description="Primary classification system used")
    burden_metric: Optional[str] = Field(None, description="Burden or importance metric used")
    data_source: Optional[str] = Field(None, description="Primary data source")
    last_updated: str = Field(..., description="Last update date (YYYY-MM-DD)")
    sources: List[str] = Field(..., description="List of authoritative sources")
    
    @validator('last_updated')
    def validate_date_format(cls, v):
        """Validate date format"""
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

class HierarchyInfo(BaseModel):
    """Hierarchical structure information"""
    structure: str = Field(..., description="Description of the hierarchical structure")
    levels: List[str] = Field(..., description="Hierarchy levels from top to bottom")
    max_depth: int = Field(..., description="Maximum depth (0-indexed)", ge=0)

# =============================================================================
# Hierarchical Item Structure
# =============================================================================

class DimensionItem(BaseModel):
    """
    Hierarchical item with path-based structure for flexible depth selection
    """
    # Core identification with hierarchical path
    id: str = Field(..., description="Full hierarchical path (e.g., 'cardiovascular/ischemic-heart-disease/mi')")
    path_components: List[str] = Field(..., description="Components of the hierarchical path")
    depth: int = Field(..., description="Depth level (0-indexed)", ge=0)
    
    # Hierarchical relationships
    parent_id: Optional[str] = Field(None, description="Parent item ID (None for root level)")
    children_ids: List[str] = Field(default_factory=list, description="Direct children item IDs")
    
    # Display information
    name: str = Field(..., description="Human-readable name for this specific level")
    description: Optional[str] = Field(None, description="Description of this item")
    
    # Level-specific metadata (preserves info from all hierarchy levels)
    level_info: Dict[int, Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Information for each level in the path"
    )
    
    # Item-specific metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Item-specific metadata")
    
    @validator('path_components')
    def path_components_match_depth(cls, v, values):
        if 'depth' in values and len(v) != values['depth'] + 1:
            raise ValueError('Path components length must equal depth + 1')
        return v
    
    @validator('id')
    def id_matches_path(cls, v, values):
        if 'path_components' in values:
            expected_id = '/'.join(values['path_components'])
            if v != expected_id:
                raise ValueError(f'ID must match path components: expected {expected_id}, got {v}')
        return v
    
    def get_ancestor_at_depth(self, target_depth: int) -> Optional[str]:
        """Get ancestor ID at specific depth"""
        if target_depth < 0 or target_depth >= len(self.path_components):
            return None
        return '/'.join(self.path_components[:target_depth + 1])
    
    def is_ancestor_of(self, other_item: 'DimensionItem') -> bool:
        """Check if this item is an ancestor of another item"""
        return other_item.id.startswith(self.id + '/')
    
    def is_descendant_of(self, other_item: 'DimensionItem') -> bool:
        """Check if this item is a descendant of another item"""
        return self.id.startswith(other_item.id + '/')
    
    def get_level_name(self, level: int) -> Optional[str]:
        """Get display name for a specific level"""
        return self.level_info.get(level, {}).get('name')

# =============================================================================
# Unified Dimension Structure
# =============================================================================

class SkillMixDimension(BaseModel):
    """Unified structure for all skill-mix dimensions with hierarchical support"""
    
    # Core identification
    dimension: DimensionType = Field(..., description="Dimension type identifier")
    description: str = Field(..., description="Brief description of the dimension")
    
    # Reference and structure information
    reference: Optional[ReferenceInfo] = Field(None, description="Reference and citation information")
    hierarchy: HierarchyInfo = Field(..., description="Hierarchical structure information")
    
    # Hierarchical items (all levels flattened with path information)
    items: List[DimensionItem] = Field(..., description="All items with hierarchical path information")
    
    # Dimension-specific global metadata
    dimension_metadata: Dict[str, Any] = Field(default_factory=dict, description="Global dimension metadata")
    
    @validator('items')
    def items_not_empty(cls, v):
        if not v:
            raise ValueError('Items list cannot be empty')
        return v
    
    @validator('items')
    def unique_item_ids(cls, v):
        ids = [item.id for item in v]
        if len(ids) != len(set(ids)):
            raise ValueError('Item IDs must be unique within dimension')
        return v
    
    @validator('items')
    def validate_hierarchy_consistency(cls, v, values):
        """Validate that parent-child relationships are consistent"""
        item_dict = {item.id: item for item in v}
        
        for item in v:
            # Check parent exists
            if item.parent_id and item.parent_id not in item_dict:
                raise ValueError(f'Parent {item.parent_id} not found for item {item.id}')
            
            # Check children exist
            for child_id in item.children_ids:
                if child_id not in item_dict:
                    raise ValueError(f'Child {child_id} not found for item {item.id}')
        
        return v

# =============================================================================
# Depth-Aware Query Functions
# =============================================================================

def get_items_at_depth(dimension: SkillMixDimension, depth: int) -> List[DimensionItem]:
    """Get all items at a specific depth level"""
    return [item for item in dimension.items if item.depth == depth]

def get_items_up_to_depth(dimension: SkillMixDimension, max_depth: int) -> List[DimensionItem]:
    """Get all items up to a maximum depth level"""
    return [item for item in dimension.items if item.depth <= max_depth]

def get_items_from_depth(dimension: SkillMixDimension, min_depth: int) -> List[DimensionItem]:
    """Get all items from a minimum depth level"""
    return [item for item in dimension.items if item.depth >= min_depth]

def get_children_at_depth(dimension: SkillMixDimension, parent_id: str, target_depth: int) -> List[DimensionItem]:
    """Get children of a specific item at target depth"""
    parent_item = next((item for item in dimension.items if item.id == parent_id), None)
    if not parent_item:
        return []
    
    return [
        item for item in dimension.items 
        if item.depth == target_depth and item.id.startswith(parent_id + '/')
    ]

def get_all_descendants(dimension: SkillMixDimension, parent_id: str) -> List[DimensionItem]:
    """Get all descendants of a specific item"""
    return [
        item for item in dimension.items 
        if item.id.startswith(parent_id + '/') and item.id != parent_id
    ]

def get_ancestors(dimension: SkillMixDimension, item_id: str) -> List[DimensionItem]:
    """Get all ancestors of a specific item"""
    target_item = next((item for item in dimension.items if item.id == item_id), None)
    if not target_item:
        return []
    
    ancestors = []
    for i in range(target_item.depth):
        ancestor_id = '/'.join(target_item.path_components[:i + 1])
        ancestor = next((item for item in dimension.items if item.id == ancestor_id), None)
        if ancestor:
            ancestors.append(ancestor)
    
    return ancestors

def expand_to_depth(dimension: SkillMixDimension, item_id: str, target_depth: int) -> List[DimensionItem]:
    """
    Expand an item to target depth
    If item is above target depth, return all descendants at target depth
    If item is at target depth, return the item itself
    If item is below target depth, return empty list
    """
    item = next((i for i in dimension.items if i.id == item_id), None)
    if not item:
        return []
    
    if item.depth == target_depth:
        return [item]
    elif item.depth < target_depth:
        return get_children_at_depth(dimension, item_id, target_depth)
    else:
        return []  # Item is deeper than target

# =============================================================================
# Multi-Dimensional Operations with Depth Control
# =============================================================================

def multiply_dimensions_at_depth(
    *dimension_depth_pairs: Tuple[SkillMixDimension, int]
) -> List[Dict[str, DimensionItem]]:
    """
    Multiply dimensions at specified depth levels
    
    Args:
        dimension_depth_pairs: Tuples of (dimension, depth_level)
        
    Returns:
        List of combination dictionaries
    """
    if not dimension_depth_pairs:
        return []
    
    # Get items at specified depths for each dimension
    dimension_items = []
    dimension_names = []
    
    for dimension, depth in dimension_depth_pairs:
        items_at_depth = get_items_at_depth(dimension, depth)
        dimension_items.append(items_at_depth)
        dimension_names.append(dimension.dimension.value)
    
    # Compute Cartesian product
    combinations = []
    for combo in product(*dimension_items):
        combination_dict = {}
        for dim_name, item in zip(dimension_names, combo):
            combination_dict[dim_name] = item
        combinations.append(combination_dict)
    
    return combinations

def multiply_dimensions_flexible_depth(
    dimension_specs: List[Dict[str, Any]]
) -> List[Dict[str, DimensionItem]]:
    """
    Multiply dimensions with flexible depth specifications
    
    Args:
        dimension_specs: List of specs, each containing:
            - dimension: SkillMixDimension
            - depth: int (optional, default: max depth)
            - filter_ids: List[str] (optional, filter to specific item IDs)
            - parent_id: str (optional, only descendants of this item)
    
    Returns:
        List of combination dictionaries
    """
    dimension_items = []
    dimension_names = []
    
    for spec in dimension_specs:
        dimension = spec['dimension']
        depth = spec.get('depth', dimension.hierarchy.max_depth)
        filter_ids = spec.get('filter_ids', [])
        parent_id = spec.get('parent_id')
        
        # Get items based on specifications
        if parent_id:
            items = get_children_at_depth(dimension, parent_id, depth)
        else:
            items = get_items_at_depth(dimension, depth)
        
        # Apply ID filter if specified
        if filter_ids:
            items = [item for item in items if item.id in filter_ids]
        
        dimension_items.append(items)
        dimension_names.append(dimension.dimension.value)
    
    # Compute Cartesian product
    combinations = []
    for combo in product(*dimension_items):
        combination_dict = {}
        for dim_name, item in zip(dimension_names, combo):
            combination_dict[dim_name] = item
        combinations.append(combination_dict)
    
    return combinations

# =============================================================================
# Helper Functions for Building Hierarchical Dimensions
# =============================================================================

def build_hierarchical_items(
    hierarchy_data: Dict[str, Any], 
    level_names: List[str],
    parent_path: List[str] = None,
    parent_id: str = None
) -> List[DimensionItem]:
    """
    Recursively build hierarchical items from nested data structure
    
    Args:
        hierarchy_data: Nested dictionary with hierarchical data
        level_names: Names of each hierarchy level
        parent_path: Current path components
        parent_id: Parent item ID
        
    Returns:
        List of DimensionItem objects
    """
    if parent_path is None:
        parent_path = []
    
    items = []
    current_depth = len(parent_path)
    
    if isinstance(hierarchy_data, dict):
        for key, value in hierarchy_data.items():
            current_path = parent_path + [key]
            current_id = '/'.join(current_path)
            
            # Create level info for all levels in path
            level_info = {}
            for i, component in enumerate(current_path):
                level_info[i] = {
                    'name': component.replace('-', ' ').title(),
                    'level_name': level_names[i] if i < len(level_names) else f'Level {i}'
                }
            
            # Determine children
            children_ids = []
            if isinstance(value, dict):
                children_ids = ['/'.join(current_path + [child_key]) for child_key in value.keys()]
            elif isinstance(value, list):
                children_ids = ['/'.join(current_path + [str(child)]) for child in value]
            
            # Create current item
            item = DimensionItem(
                id=current_id,
                path_components=current_path,
                depth=current_depth,
                parent_id=parent_id,
                children_ids=children_ids,
                name=key.replace('-', ' ').title(),
                level_info=level_info,
                metadata={}
            )
            items.append(item)
            
            # Recursively process children
            if isinstance(value, (dict, list)):
                child_items = build_hierarchical_items(
                    value, level_names, current_path, current_id
                )
                items.extend(child_items)
            
    elif isinstance(hierarchy_data, list):
        for item_data in hierarchy_data:
            if isinstance(item_data, str):
                current_path = parent_path + [item_data]
                current_id = '/'.join(current_path)
                
                level_info = {}
                for i, component in enumerate(current_path):
                    level_info[i] = {
                        'name': component.replace('-', ' ').title(),
                        'level_name': level_names[i] if i < len(level_names) else f'Level {i}'
                    }
                
                item = DimensionItem(
                    id=current_id,
                    path_components=current_path,
                    depth=current_depth,
                    parent_id=parent_id,
                    children_ids=[],
                    name=item_data.replace('-', ' ').title(),
                    level_info=level_info,
                    metadata={}
                )
                items.append(item)
    
    return items

# =============================================================================
# Example Usage and Testing
# =============================================================================

if __name__ == "__main__":
    # Example: Create a hierarchical diseases dimension
    diseases_hierarchy = {
        'cardiovascular': {
            'ischemic-heart-disease': ['myocardial-infarction', 'angina-pectoris'],
            'stroke': ['ischemic-stroke', 'hemorrhagic-stroke']
        },
        'respiratory': {
            'copd': ['emphysema', 'chronic-bronchitis'],
            'asthma': ['allergic-asthma', 'non-allergic-asthma']
        }
    }
    
    level_names = ['chapter', 'condition', 'subtype']
    items = build_hierarchical_items(diseases_hierarchy, level_names)
    
    diseases_dimension = SkillMixDimension(
        dimension=DimensionType.DISEASES,
        description="Hierarchical disease categories",
        hierarchy=HierarchyInfo(
            structure="Chapter -> Condition -> Subtype",
            levels=level_names,
            max_depth=2
        ),
        items=items
    )
    
    print(f"✓ Created diseases dimension with {len(diseases_dimension.items)} items")
    print(f"✓ Max depth: {diseases_dimension.hierarchy.max_depth}")
    
    # Test depth queries
    chapters = get_items_at_depth(diseases_dimension, 0)
    print(f"✓ Chapters (depth 0): {[item.name for item in chapters]}")
    
    conditions = get_items_at_depth(diseases_dimension, 1)
    print(f"✓ Conditions (depth 1): {[item.name for item in conditions]}")
    
    subtypes = get_items_at_depth(diseases_dimension, 2)
    print(f"✓ Subtypes (depth 2): {[item.name for item in subtypes]}")
    
    # Test expansion
    cardio_subtypes = expand_to_depth(diseases_dimension, 'cardiovascular', 2)
    print(f"✓ Cardiovascular subtypes: {[item.name for item in cardio_subtypes]}")
    
    print("✓ Hierarchical dimension model working correctly!")