#!/usr/bin/env python3
"""
Generate assigned_authority.json for the AI Cognitive Engagement Cube (3A)
Assigned Authority specifies the degree of AI cognitive takeover
"""

import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "clinical-skill-mix"))

from skill_mix_dimensions_model import (
    SkillMixDimension, DimensionItem, ReferenceInfo, HierarchyInfo, DimensionType
)

# Define paths
BASE_PATH = Path(__file__).parent.parent
SKILL_MIX_PATH = BASE_PATH / "clinical-skill-mix"

def create_assigned_authority_items():
    """Create the assigned authority dimension items"""

    authority_data = [
        {
            "id": "monitoring",
            "order": 1,
            "name": "Monitoring",
            "description": "AI observes and flags issues for human review without direct action",
            "ai_role": "Observer",
            "human_role": "Primary decision-maker and executor",
            "control_level": "Human-in-command",
            "example_applications": [
                "Clinical surveillance systems",
                "Quality monitoring dashboards",
                "Adverse event detection",
                "Performance metrics tracking"
            ],
            "autonomy_level": "Minimal (AI provides information only)"
        },
        {
            "id": "augmentation",
            "order": 2,
            "name": "Augmentation",
            "description": "AI provides supportive recommendations while human retains decision authority",
            "ai_role": "Supportive contributor",
            "human_role": "Final decision-maker with AI assistance",
            "control_level": "Human-on-the-loop",
            "example_applications": [
                "Clinical decision support systems",
                "Diagnostic assistance tools",
                "Treatment recommendation engines",
                "Risk stratification tools"
            ],
            "autonomy_level": "Moderate (AI suggests, human decides)"
        },
        {
            "id": "automation",
            "order": 3,
            "name": "Automation",
            "description": "AI executes decisions autonomously with human oversight for exceptions",
            "ai_role": "Primary processor",
            "human_role": "Overseer and exception handler",
            "control_level": "Human-out-of-the-loop",
            "example_applications": [
                "Automated medication dispensing",
                "Robotic surgery systems",
                "Autonomous diagnostic imaging analysis",
                "Automated appointment scheduling"
            ],
            "autonomy_level": "High (AI executes, human monitors)"
        }
    ]

    items = []
    for authority in authority_data:
        item = DimensionItem(
            id=authority["id"],
            path_components=[authority["id"]],
            depth=0,
            parent_id=None,
            children_ids=[],
            name=authority["name"],
            description=authority["description"],
            level_info={
                0: {
                    "name": authority["name"],
                    "level_name": "Authority Level"
                }
            },
            metadata={
                "order": authority["order"],
                "ai_role": authority["ai_role"],
                "human_role": authority["human_role"],
                "control_level": authority["control_level"],
                "autonomy_level": authority["autonomy_level"],
                "example_applications": authority["example_applications"]
            }
        )
        items.append(item)

    return items

def generate_assigned_authority_dimension():
    """Generate the complete assigned authority dimension"""

    items = create_assigned_authority_items()

    dimension = SkillMixDimension(
        dimension=DimensionType.ASSIGNED_AUTHORITY,
        description="Specifies the degree of AI cognitive takeover in clinical tasks, ranging from passive monitoring through active augmentation to full automation. Defines the balance of authority between human and AI in decision-making and execution.",
        reference=ReferenceInfo(
            classification="Assigned Authority Framework: Three Levels of AI Autonomy",
            burden_metric="Degree of AI autonomy and human oversight requirements",
            data_source="Human-AI collaboration frameworks and automation taxonomies",
            last_updated="2026-02-04",
            sources=[
                "Levels of Automation (Sheridan & Verplank): Information, recommendation, execution",
                "Human-in-the-loop vs Human-on-the-loop vs Human-out-of-the-loop",
                "FDA guidance on clinical decision support and AI autonomy",
                "Clinical AI integration models"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Progressive levels of AI autonomy from monitoring to automation",
            levels=["authority"],
            max_depth=0
        ),
        items=items
    )

    return dimension

def save_dimension(dimension):
    """Save the assigned authority dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'assigned_authority.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated assigned_authority.json with {len(dimension.items)} authority levels")
    print(f"✓ Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating assigned authority dimension...")
    print("=" * 60)

    try:
        dimension = generate_assigned_authority_dimension()
        output_path = save_dimension(dimension)

        print("=" * 60)
        print("✓ Assigned authority dimension generation complete!")
        print(f"\nAuthority levels included:")
        for item in dimension.items:
            print(f"  {item.metadata['order']}. {item.name} ({item.id}) - {item.metadata['ai_role']}")

    except Exception as e:
        print(f"❌ Error generating assigned_authority.json: {e}")
        raise
