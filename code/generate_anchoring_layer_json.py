#!/usr/bin/env python3
"""
Generate anchoring_layer.json for the AI Cognitive Engagement Cube (3A)
Anchoring Layer specifies the point in cognitive architecture where AI intervenes
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

def create_anchoring_layer_items():
    """Create the anchoring layer dimension items"""

    layers_data = [
        {
            "id": "input",
            "order": 1,
            "name": "Input",
            "description": "Clinical data gathering and acquisition layer",
            "cdm_function": "Encounter data collection, patient records, clinical observations",
            "example_ai_applications": [
                "Voice-to-text documentation",
                "Automated data extraction from EHR",
                "Sensor data integration",
                "Patient-reported outcome capture"
            ]
        },
        {
            "id": "data_processor",
            "order": 2,
            "name": "Data Processor",
            "description": "Evidence-guided synthesis and information processing",
            "cdm_function": "Transform raw inputs into clinically meaningful cues",
            "example_ai_applications": [
                "Lab result interpretation",
                "Vital sign trend analysis",
                "Clinical note summarization",
                "Risk score calculation"
            ]
        },
        {
            "id": "hypothesis",
            "order": 3,
            "name": "Hypothesis",
            "description": "Differential diagnosis formulation and hypothesis generation",
            "cdm_function": "Generate and refine diagnostic possibilities",
            "example_ai_applications": [
                "Differential diagnosis generators",
                "Diagnostic suggestion systems",
                "Symptom-to-diagnosis mapping",
                "Clinical reasoning support"
            ]
        },
        {
            "id": "system_i",
            "order": 4,
            "name": "System I",
            "description": "Illness script activation and pattern recognition (intuition)",
            "cdm_function": "Fast, automatic pattern matching based on clinical experience",
            "example_ai_applications": [
                "Image recognition for radiology",
                "Pattern-based alert systems",
                "Rapid triage support",
                "Clinical pattern identification"
            ]
        },
        {
            "id": "system_ii",
            "order": 5,
            "name": "System II",
            "description": "Hypothetico-deductive analytical reasoning (deliberation)",
            "cdm_function": "Slow, deliberate analysis using evidence-based reasoning",
            "example_ai_applications": [
                "Evidence-based treatment recommendations",
                "Guideline compliance checking",
                "Complex case analysis",
                "Probabilistic diagnostic reasoning"
            ]
        },
        {
            "id": "reflection",
            "order": 6,
            "name": "Reflection",
            "description": "Metacognitive monitoring and bias detection",
            "cdm_function": "Self-awareness of reasoning quality and potential errors",
            "example_ai_applications": [
                "Cognitive bias alerts",
                "Second opinion systems",
                "Diagnostic error detection",
                "Clinical reasoning audit tools"
            ]
        },
        {
            "id": "action",
            "order": 7,
            "name": "Action",
            "description": "Care plan execution and decision implementation",
            "cdm_function": "Translate decisions into clinical actions",
            "example_ai_applications": [
                "Order entry optimization",
                "Treatment pathway execution",
                "Medication prescribing support",
                "Procedure scheduling automation"
            ]
        }
    ]

    items = []
    for layer in layers_data:
        item = DimensionItem(
            id=layer["id"],
            path_components=[layer["id"]],
            depth=0,
            parent_id=None,
            children_ids=[],
            name=layer["name"],
            description=layer["description"],
            level_info={
                0: {
                    "name": layer["name"],
                    "level_name": "Cognitive Layer"
                }
            },
            metadata={
                "order": layer["order"],
                "cdm_function": layer["cdm_function"],
                "example_ai_applications": layer["example_ai_applications"],
                "reasoning_type": "Fast/Intuitive" if layer["id"] == "system_i" else "Slow/Analytical" if layer["id"] == "system_ii" else "Sequential"
            }
        )
        items.append(item)

    return items

def generate_anchoring_layer_dimension():
    """Generate the complete anchoring layer dimension"""

    items = create_anchoring_layer_items()

    dimension = SkillMixDimension(
        dimension=DimensionType.ANCHORING_LAYER,
        description="Specifies the point in cognitive architecture where AI intervenes, from initial data input through hypothesis generation, dual-process reasoning (System I/II), reflection, to action execution. Based on the CDM cognitive framework.",
        reference=ReferenceInfo(
            classification="Anchoring Layer Framework: Seven Cognitive Processing Stages",
            burden_metric="Cognitive depth and reasoning complexity",
            data_source="Clinician Decision Making (CDM) cognitive architecture",
            last_updated="2026-02-04",
            sources=[
                "CDM Framework: Input → Data Processor → Hypothesis → System I/II → Reflection → Action",
                "Dual-process theory (Kahneman): System I (intuition) and System II (analysis)",
                "Clinical reasoning models",
                "Cognitive load theory in healthcare"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Sequential cognitive processing layers from input to action",
            levels=["layer"],
            max_depth=0
        ),
        items=items
    )

    return dimension

def save_dimension(dimension):
    """Save the anchoring layer dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'anchoring_layer.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated anchoring_layer.json with {len(dimension.items)} cognitive layers")
    print(f"✓ Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating anchoring layer dimension...")
    print("=" * 60)

    try:
        dimension = generate_anchoring_layer_dimension()
        output_path = save_dimension(dimension)

        print("=" * 60)
        print("✓ Anchoring layer dimension generation complete!")
        print(f"\nCognitive layers included:")
        for item in dimension.items:
            print(f"  {item.metadata['order']}. {item.name} ({item.id})")

    except Exception as e:
        print(f"❌ Error generating anchoring_layer.json: {e}")
        raise
