#!/usr/bin/env python3
"""
Count values within each dimension of the Clinical World Model
Analyzes all 8 dimensions (5C + 3A) and provides detailed statistics
"""

import json
from pathlib import Path
from collections import defaultdict

# Define paths
BASE_PATH = Path(__file__).parent.parent.parent
SKILL_MIX_PATH = BASE_PATH / "clinical-skill-mix"

# All 8 dimensions
DIMENSIONS = [
    # Clinical Competency Space (5C)
    "conditions",
    "care_phases",
    "care_settings",
    "care_task",
    "care_provider_role",
    # AI Cognitive Engagement (3A)
    "agent_facing",
    "anchoring_layer",
    "assigned_authority"
]

def analyze_dimension(dimension_name):
    """Analyze a single dimension and return statistics"""
    json_file = SKILL_MIX_PATH / f"{dimension_name}.json"

    if not json_file.exists():
        return None

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data.get('items', [])

    # Count by depth
    depth_counts = defaultdict(int)
    for item in items:
        depth = item.get('depth', 0)
        depth_counts[depth] += 1

    # Get hierarchy info
    hierarchy = data.get('hierarchy', {})
    max_depth = hierarchy.get('max_depth', 0)
    levels = hierarchy.get('levels', [])

    return {
        'dimension': data.get('dimension', dimension_name),
        'description': data.get('description', '')[:100] + '...',
        'total_items': len(items),
        'depth_counts': dict(depth_counts),
        'max_depth': max_depth,
        'hierarchy_levels': levels,
        'reference': data.get('reference', {})
    }

def print_separator(char='=', length=80):
    """Print a separator line"""
    print(char * length)

def main():
    """Main analysis function"""
    print_separator('=')
    print("CLINICAL WORLD MODEL - DIMENSION VALUE COUNTS")
    print_separator('=')
    print()

    # Analyze all dimensions
    results_5c = []
    results_3a = []

    for dim_name in DIMENSIONS:
        result = analyze_dimension(dim_name)
        if result:
            if dim_name in ["conditions", "care_phases", "care_settings", "care_task", "care_provider_role"]:
                results_5c.append(result)
            else:
                results_3a.append(result)

    # Print 5C results
    print("CLINICAL COMPETENCY SPACE (5C)")
    print_separator('-')
    print()

    total_5c = 0
    for result in results_5c:
        print(f"[{result['dimension'].upper()}]")
        print(f"   Total Items: {result['total_items']}")

        if result['depth_counts']:
            print(f"   Breakdown by depth:")
            for depth in sorted(result['depth_counts'].keys()):
                count = result['depth_counts'][depth]
                level_name = result['hierarchy_levels'][depth] if depth < len(result['hierarchy_levels']) else f"depth_{depth}"
                print(f"      - Depth {depth} ({level_name}): {count}")

        if result['hierarchy_levels']:
            print(f"   Hierarchy: {' > '.join(result['hierarchy_levels'])}")

        print(f"   Max Depth: {result['max_depth']}")

        if result['reference']:
            classification = result['reference'].get('classification', 'N/A')
            print(f"   Source: {classification}")

        print()
        total_5c += result['total_items']

    print(f"TOTAL 5C ITEMS: {total_5c}")
    print()
    print_separator('=')
    print()

    # Print 3A results
    print("AI COGNITIVE ENGAGEMENT (3A)")
    print_separator('-')
    print()

    total_3a = 0
    for result in results_3a:
        print(f"[{result['dimension'].upper()}]")
        print(f"   Total Items: {result['total_items']}")

        if result['depth_counts']:
            print(f"   Breakdown by depth:")
            for depth in sorted(result['depth_counts'].keys()):
                count = result['depth_counts'][depth]
                print(f"      - Depth {depth}: {count}")

        print()
        total_3a += result['total_items']

    print(f"TOTAL 3A ITEMS: {total_3a}")
    print()
    print_separator('=')
    print()

    # Calculate Clinical Intelligence Space
    print("CLINICAL INTELLIGENCE SPACE CALCULATIONS")
    print_separator('-')
    print()

    # Get leaf node counts for 5C
    conditions_leaf = results_5c[0]['depth_counts'].get(1, 0)  # conditions at depth 1
    care_phases = results_5c[1]['total_items']  # all phases (flat)
    care_settings = results_5c[2]['total_items']  # all settings (flat)
    care_task_leaf = results_5c[3]['depth_counts'].get(1, 0)  # tasks at depth 1
    care_provider_all = results_5c[4]['total_items']  # ALL provider roles (86 total)

    # Get counts for 3A (all flat)
    agent_facing = results_3a[0]['total_items']
    anchoring_layer = results_3a[1]['total_items']
    assigned_authority = results_3a[2]['total_items']

    # Calculate cells
    clinical_competency_cells = conditions_leaf * care_phases * care_settings * care_task_leaf * care_provider_all
    ai_engagement_patterns = agent_facing * anchoring_layer * assigned_authority
    total_intelligence_cells = clinical_competency_cells * ai_engagement_patterns

    print(f"Clinical Competency (5C) Calculation:")
    print(f"  {conditions_leaf:,} conditions × {care_phases} phases × {care_settings} settings × {care_task_leaf} tasks × {care_provider_all} providers")
    print(f"  = {clinical_competency_cells:,} clinical scenarios")
    print()

    print(f"AI Cognitive Engagement (3A) Calculation:")
    print(f"  {agent_facing} agent facing × {anchoring_layer} layers × {assigned_authority} authority")
    print(f"  = {ai_engagement_patterns} AI engagement patterns")
    print()

    print(f"Clinical Intelligence Space (5C × 3A):")
    print(f"  {clinical_competency_cells:,} × {ai_engagement_patterns}")
    print(f"  = {total_intelligence_cells:,} unique Clinical Intelligence cells")
    print(f"  = {total_intelligence_cells / 1_000_000_000:.1f} billion cells")
    print()

    print_separator('=')
    print()

    # Summary
    print("SUMMARY")
    print_separator('-')
    print(f"Total dimension items across 8 dimensions: {total_5c + total_3a:,}")
    print(f"  - Clinical Competency (5C): {total_5c:,} items")
    print(f"  - AI Cognitive Engagement (3A): {total_3a:,} items")
    print()
    print(f"Clinical Intelligence Space:")
    print(f"  - Clinical scenarios (5C): {clinical_competency_cells:,} ({clinical_competency_cells / 1_000_000:.1f}M)")
    print(f"  - AI engagement patterns (3A): {ai_engagement_patterns}")
    print(f"  - Total cells (5C × 3A): {total_intelligence_cells:,} ({total_intelligence_cells / 1_000_000_000:.1f}B)")
    print()
    print_separator('=')

if __name__ == "__main__":
    main()
