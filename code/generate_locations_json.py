#!/usr/bin/env python3
"""
Generate location.json for the Clinical Skill-Mix Cube
Location of care is intrinsically linked to disease stage
Settings range from community to intensive care
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

def create_location_items():
    """Create the location of care items with metadata"""

    locations_data = [
        {
            "id": "community",
            "name": "Community",
            "description": "Community-based health services, public health programs, and population-level interventions",
            "care_type": "Preventive and population health",
            "acuity": "Low",
            "typical_stages": ["at-risk", "follow-up", "coping"],
            "resource_intensity": "Low to moderate",
            "patient_volume": "High"
        },
        {
            "id": "home",
            "name": "Home",
            "description": "Home-based care including home health services, remote monitoring, and family-delivered care",
            "care_type": "Chronic disease management and recovery",
            "acuity": "Low to moderate",
            "typical_stages": ["at-risk", "post-treatment-care", "follow-up", "coping"],
            "resource_intensity": "Low to moderate",
            "patient_volume": "Moderate"
        },
        {
            "id": "telemedicine",
            "name": "Tele-medicine",
            "description": "Virtual care delivery through telecommunications technology, remote consultations, and digital health platforms",
            "care_type": "Remote consultation and monitoring",
            "acuity": "Low to moderate",
            "typical_stages": ["at-risk", "pre-symptomatic", "treatment-planning", "follow-up"],
            "resource_intensity": "Low",
            "patient_volume": "High"
        },
        {
            "id": "long-term-care",
            "name": "Long-term Care Center",
            "description": "Facilities providing extended care for chronic conditions, rehabilitation, and palliative care",
            "care_type": "Long-term and palliative care",
            "acuity": "Low to moderate",
            "typical_stages": ["post-treatment-care", "follow-up", "coping"],
            "resource_intensity": "Moderate",
            "patient_volume": "Moderate"
        },
        {
            "id": "clinic",
            "name": "Clinic",
            "description": "Outpatient clinics for primary care, specialist consultations, and follow-up visits",
            "care_type": "Outpatient evaluation and management",
            "acuity": "Low to moderate",
            "typical_stages": ["at-risk", "pre-symptomatic", "diagnostic-workup", "treatment-planning", "follow-up"],
            "resource_intensity": "Moderate",
            "patient_volume": "High"
        },
        {
            "id": "pre-hospital-care",
            "name": "Pre-hospital Care",
            "description": "Emergency medical services, ambulance care, and first responder services before hospital arrival",
            "care_type": "Emergency response and stabilization",
            "acuity": "Moderate to critical",
            "typical_stages": ["diagnostic-workup"],
            "resource_intensity": "Moderate to high",
            "patient_volume": "Moderate"
        },
        {
            "id": "diagnostic-facility",
            "name": "Diagnostic Facility",
            "description": "Facilities dedicated to diagnostic testing including imaging centers, laboratories, and diagnostic procedure units",
            "care_type": "Diagnostic evaluation",
            "acuity": "Low to moderate",
            "typical_stages": ["pre-symptomatic", "diagnostic-workup", "follow-up"],
            "resource_intensity": "High (technology-intensive)",
            "patient_volume": "High"
        },
        {
            "id": "procedure-facility",
            "name": "Procedure Facility",
            "description": "Ambulatory surgery centers and outpatient procedure units for minor interventions",
            "care_type": "Outpatient procedures",
            "acuity": "Moderate",
            "typical_stages": ["treatment-planning", "post-treatment-care"],
            "resource_intensity": "Moderate to high",
            "patient_volume": "Moderate"
        },
        {
            "id": "operation-room",
            "name": "Operation Room",
            "description": "Surgical theaters for major operative procedures requiring anesthesia and surgical teams",
            "care_type": "Surgical intervention",
            "acuity": "High to critical",
            "typical_stages": ["treatment-planning"],
            "resource_intensity": "Very high",
            "patient_volume": "Moderate"
        },
        {
            "id": "emergency-room",
            "name": "Emergency Room",
            "description": "Emergency departments providing urgent and emergent care for acute conditions",
            "care_type": "Emergency evaluation and stabilization",
            "acuity": "Moderate to critical",
            "typical_stages": ["diagnostic-workup", "treatment-planning"],
            "resource_intensity": "High",
            "patient_volume": "High"
        },
        {
            "id": "ward",
            "name": "Ward",
            "description": "General inpatient hospital wards for acute medical and surgical care",
            "care_type": "Inpatient medical and surgical care",
            "acuity": "Moderate to high",
            "typical_stages": ["diagnostic-workup", "treatment-planning", "post-treatment-care"],
            "resource_intensity": "High",
            "patient_volume": "High"
        },
        {
            "id": "intensive-care-units",
            "name": "Intensive Care Units",
            "description": "Critical care units providing continuous monitoring and life support for critically ill patients",
            "care_type": "Critical care and life support",
            "acuity": "Critical",
            "typical_stages": ["treatment-planning", "post-treatment-care"],
            "resource_intensity": "Very high",
            "patient_volume": "Low to moderate"
        }
    ]

    items = []
    for location in locations_data:
        item = DimensionItem(
            id=location["id"],
            path_components=[location["id"]],
            depth=0,
            parent_id=None,
            children_ids=[],
            name=location["name"],
            description=location["description"],
            level_info={
                0: {
                    "name": location["name"],
                    "level_name": "Care Setting"
                }
            },
            metadata={
                "care_type": location["care_type"],
                "acuity": location["acuity"],
                "typical_stages": location["typical_stages"],
                "resource_intensity": location["resource_intensity"],
                "patient_volume": location["patient_volume"]
            }
        )
        items.append(item)

    return items

def generate_location_dimension():
    """Generate the complete location dimension"""

    items = create_location_items()

    dimension = SkillMixDimension(
        dimension=DimensionType.LOCATION,
        description="Location of care is intrinsically linked to disease stage, as different stages typically occur in distinct settings ranging from community screening to emergency departments, inpatient wards, intensive care units, rehabilitation facilities, and home-based care.",
        reference=ReferenceInfo(
            classification="Care Delivery Settings and Patient Journey Mapping",
            burden_metric="Care complexity and resource intensity across 12 settings",
            data_source="Healthcare delivery models and patient journey frameworks",
            last_updated="2025-01-30",
            sources=[
                "SEIPS Framework: Systems Engineering Initiative for Patient Safety (patient journey modeling)",
                "Healthcare facility classification systems",
                "Care delivery settings: Community to emergency to ICU to rehabilitation to home",
                "Resource allocation and capacity planning frameworks"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Care location settings integrated with disease stage progression",
            levels=["location"],
            max_depth=0
        ),
        items=items
    )

    return dimension

def save_dimension(dimension):
    """Save the location dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'location.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated location.json with {len(dimension.items)} locations")
    print(f"✓ Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating location of care dimension...")
    print("=" * 60)

    try:
        dimension = generate_location_dimension()
        output_path = save_dimension(dimension)

        print("=" * 60)
        print("✓ Location dimension generation complete!")
        print(f"\nLocations included:")
        for item in dimension.items:
            print(f"  - {item.name} ({item.id}) - {item.metadata['acuity']} acuity")

    except Exception as e:
        print(f"❌ Error generating location.json: {e}")
        raise
