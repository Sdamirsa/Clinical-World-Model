#!/usr/bin/env python3
"""
Generate agent_facing.json for the AI Cognitive Engagement Cube (3A)
Agent Facing defines whose cognition AI engages (provider/patient/encounter)
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

def create_agent_facing_items():
    """Create the agent facing dimension items"""

    agents_data = [
        {
            "id": "provider_facing",
            "name": "Provider-Facing",
            "description": "AI engages with healthcare provider's cognitive processes (CDM model)",
            "cognitive_model": "Clinician Decision Making (CDM)",
            "primary_user": "Healthcare professionals",
            "example_applications": [
                "Clinical decision support systems",
                "Diagnostic assistance tools",
                "Treatment planning aids",
                "Medical documentation automation"
            ]
        },
        {
            "id": "patient_facing",
            "name": "Patient-Facing",
            "description": "AI engages with patient's cognitive processes (PDM model)",
            "cognitive_model": "Patient Decision Making (PDM)",
            "primary_user": "Patients and caregivers",
            "example_applications": [
                "Patient education platforms",
                "Symptom checkers",
                "Shared decision-making tools",
                "Self-management apps"
            ]
        },
        {
            "id": "encounter_facing",
            "name": "Encounter-Facing",
            "description": "AI engages with system-level clinical encounter (CDM + PDM integration)",
            "cognitive_model": "Integrated CDM + PDM",
            "primary_user": "Healthcare system / encounter workflow",
            "example_applications": [
                "Encounter workflow optimization",
                "Communication facilitation tools",
                "Coordination platforms",
                "Integrated care pathway systems"
            ]
        }
    ]

    items = []
    for agent in agents_data:
        item = DimensionItem(
            id=agent["id"],
            path_components=[agent["id"]],
            depth=0,
            parent_id=None,
            children_ids=[],
            name=agent["name"],
            description=agent["description"],
            level_info={
                0: {
                    "name": agent["name"],
                    "level_name": "Agent Type"
                }
            },
            metadata={
                "cognitive_model": agent["cognitive_model"],
                "primary_user": agent["primary_user"],
                "example_applications": agent["example_applications"]
            }
        )
        items.append(item)

    return items

def generate_agent_facing_dimension():
    """Generate the complete agent facing dimension"""

    items = create_agent_facing_items()

    dimension = SkillMixDimension(
        dimension=DimensionType.AGENT_FACING,
        description="Defines whose cognition AI engages: provider (CDM), patient (PDM), or encounter (system-level integration). This dimension specifies the primary cognitive agent interacting with AI in the clinical workflow.",
        reference=ReferenceInfo(
            classification="Agent Facing Framework: Three Cognitive Engagement Types",
            burden_metric="User perspective and cognitive model integration",
            data_source="Clinical decision-making models (CDM/PDM framework)",
            last_updated="2026-02-04",
            sources=[
                "Clinician Decision Making (CDM) model",
                "Patient Decision Making (PDM) model",
                "Clinical encounter workflow frameworks",
                "Human-AI interaction patterns in healthcare"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Flat list of three agent types",
            levels=["agent"],
            max_depth=0
        ),
        items=items
    )

    return dimension

def save_dimension(dimension):
    """Save the agent facing dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'agent_facing.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated agent_facing.json with {len(dimension.items)} agent types")
    print(f"✓ Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating agent facing dimension...")
    print("=" * 60)

    try:
        dimension = generate_agent_facing_dimension()
        output_path = save_dimension(dimension)

        print("=" * 60)
        print("✓ Agent facing dimension generation complete!")
        print(f"\nAgent types included:")
        for item in dimension.items:
            print(f"  - {item.name} ({item.id})")

    except Exception as e:
        print(f"❌ Error generating agent_facing.json: {e}")
        raise
