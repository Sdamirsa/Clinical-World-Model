#!/usr/bin/env python3
"""
Generate stage.json for the Clinical Skill-Mix Cube
Disease stage represents the temporal dimension of illness
Seven milestones and six actionable stages spanning the patient journey
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

def create_stage_items():
    """Create the disease stage items with metadata"""

    stages_data = [
        {
            "id": "at-risk",
            "name": "At-Risk Identification",
            "description": "Identification of individuals at increased risk before disease manifestation",
            "milestone": "Health → Pathologic process",
            "interventions": ["Risk assessment", "Primary prevention", "Lifestyle modification"],
            "typical_locations": ["Community", "Clinic", "Tele-medicine"],
            "reversible": True,
            "temporal_position": 1
        },
        {
            "id": "pre-symptomatic",
            "name": "Pre-Symptomatic Detection",
            "description": "Detection of pathologic process before symptom manifestation",
            "milestone": "Pathologic process → Illness manifestation",
            "interventions": ["Screening", "Early detection", "Biomarker monitoring"],
            "typical_locations": ["Clinic", "Diagnostic facility", "Community"],
            "reversible": True,
            "temporal_position": 2
        },
        {
            "id": "diagnostic-workup",
            "name": "Diagnostic Workup",
            "description": "Comprehensive evaluation to establish diagnosis after illness manifestation",
            "milestone": "Illness manifestation → Diagnosis",
            "interventions": ["Diagnostic testing", "Imaging", "Clinical evaluation", "Differential diagnosis"],
            "typical_locations": ["Emergency room", "Clinic", "Diagnostic facility", "Ward"],
            "reversible": False,
            "temporal_position": 3
        },
        {
            "id": "treatment-planning",
            "name": "Treatment Planning",
            "description": "Development of therapeutic strategy following diagnosis",
            "milestone": "Diagnosis → Treatment",
            "interventions": ["Treatment selection", "Shared decision-making", "Risk-benefit analysis", "Resource allocation"],
            "typical_locations": ["Clinic", "Ward", "Tele-medicine"],
            "reversible": False,
            "temporal_position": 4
        },
        {
            "id": "post-treatment-care",
            "name": "Post-Treatment Care",
            "description": "Immediate care following therapeutic intervention",
            "milestone": "Treatment → Follow-up",
            "interventions": ["Complication monitoring", "Recovery support", "Rehabilitation", "Medication management"],
            "typical_locations": ["Ward", "Intensive care units", "Long-term care center", "Home"],
            "reversible": False,
            "temporal_position": 5
        },
        {
            "id": "follow-up",
            "name": "Longitudinal Follow-Up",
            "description": "Ongoing monitoring and disease surveillance",
            "milestone": "Follow-up → Outcomes assessment",
            "interventions": ["Surveillance", "Recurrence detection", "Chronic disease management", "Secondary prevention"],
            "typical_locations": ["Clinic", "Tele-medicine", "Home", "Community"],
            "reversible": False,
            "temporal_position": 6
        },
        {
            "id": "coping",
            "name": "Coping Support",
            "description": "Psychosocial support for living with disease outcomes (disability, chronic illness, end-of-life)",
            "milestone": "Follow-up → Cure/Disability/Death",
            "interventions": ["Palliative care", "Psychosocial support", "Advance care planning", "Caregiver support"],
            "typical_locations": ["Home", "Long-term care center", "Clinic", "Community"],
            "reversible": False,
            "temporal_position": 7
        }
    ]

    items = []
    for stage in stages_data:
        item = DimensionItem(
            id=stage["id"],
            path_components=[stage["id"]],
            depth=0,
            parent_id=None,
            children_ids=[],
            name=stage["name"],
            description=stage["description"],
            level_info={
                0: {
                    "name": stage["name"],
                    "level_name": "Actionable Stage"
                }
            },
            metadata={
                "milestone": stage["milestone"],
                "interventions": stage["interventions"],
                "typical_locations": stage["typical_locations"],
                "reversible": stage["reversible"],
                "temporal_position": stage["temporal_position"],
                "note": "Patients may occupy multiple stages simultaneously"
            }
        )
        items.append(item)

    return items

def generate_stage_dimension():
    """Generate the complete stage dimension"""

    items = create_stage_items()

    dimension = SkillMixDimension(
        dimension=DimensionType.STAGE,
        description="Disease stage represents the temporal dimension of illness, characterized through seven milestones and six actionable stages spanning the continuum from health through pathologic process, illness manifestation, diagnosis, treatment, follow-up, to final outcomes. Patients may occupy multiple positions simultaneously.",
        reference=ReferenceInfo(
            classification="Disease Stage Framework: Seven Milestones and Six Actionable Stages",
            burden_metric="Clinical significance across patient journey",
            data_source="Clinical pathophysiology and patient journey models",
            last_updated="2025-01-30",
            sources=[
                "Seven Milestones: Health → Pathologic process → Illness manifestation → Diagnosis → Treatment → Follow-up → (Cure/Disability/Death)",
                "Six Actionable Stages: At-risk identification, Pre-symptomatic detection, Diagnostic workup, Treatment planning, Post-treatment care, Longitudinal follow-up/coping",
                "SEIPS Framework: Systems Engineering Initiative for Patient Safety",
                "Clinical pathway and patient journey frameworks"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Seven disease stage milestones with actionable intervention points",
            levels=["stage"],
            max_depth=0
        ),
        items=items
    )

    return dimension

def save_dimension(dimension):
    """Save the stage dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'stage.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated stage.json with {len(dimension.items)} stages")
    print(f"✓ Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating disease stage dimension...")
    print("=" * 60)

    try:
        dimension = generate_stage_dimension()
        output_path = save_dimension(dimension)

        print("=" * 60)
        print("✓ Stage dimension generation complete!")
        print(f"\nStages included:")
        for item in dimension.items:
            print(f"  - {item.name} ({item.id})")

    except Exception as e:
        print(f"❌ Error generating stage.json: {e}")
        raise
