#!/usr/bin/env python3
"""
Generate care_task.json for the Clinical Competency Cube (5C)
Care tasks represent cognitive activities for AI augmentation/automation
Based on Physician Competency Reference Set (Englander et al.)
"""

import json
import csv
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "clinical-skill-mix"))

from skill_mix_dimensions_model import (
    SkillMixDimension, DimensionItem, ReferenceInfo, HierarchyInfo, DimensionType
)

# Define paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data"
SKILL_MIX_PATH = BASE_PATH / "clinical-skill-mix"

def load_enhanced_competencies():
    """Load the enhanced competency CSV with AI interaction modes"""
    csv_path = DATA_PATH / "Physician Competency Reference Set - Enhanced.csv"

    competencies = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            competencies.append(row)

    return competencies

def create_task_items():
    """Create task items from the enhanced competency data"""

    competencies = load_enhanced_competencies()

    # Group by category to create parent items
    categories = {}
    for comp in competencies:
        cat = comp['Category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(comp)

    items = []

    # Category mapping for IDs and descriptions
    category_info = {
        "Patient Care": {
            "id": "patient-care",
            "description": "Core clinical activities including procedures, data gathering, decision-making, and patient education",
            "domain_number": 1
        },
        "Knowledge for Practice": {
            "id": "knowledge-practice",
            "description": "Application of biomedical, clinical, epidemiological, and social-behavioral sciences to patient care",
            "domain_number": 2
        },
        "Practice-Based Learning and Improvement": {
            "id": "practice-learning",
            "description": "Self-assessment, quality improvement, evidence appraisal, and continuous professional development",
            "domain_number": 3
        },
        "Interpersonal & Communication Skills": {
            "id": "communication",
            "description": "Effective communication with patients, families, colleagues, and maintaining medical records",
            "domain_number": 4
        },
        "Professionalism": {
            "id": "professionalism",
            "description": "Ethical practice, compassion, accountability, and respect for diversity and patient autonomy",
            "domain_number": 5
        },
        "System-based Practice": {
            "id": "systems-practice",
            "description": "Healthcare system navigation, care coordination, resource stewardship, and quality advocacy",
            "domain_number": 6
        },
        "Interperprofessional Collaboration": {
            "id": "interprofessional",
            "description": "Collaborative practice with other health professionals in team-based care delivery",
            "domain_number": 7
        },
        "Personal & Professional Development": {
            "id": "personal-development",
            "description": "Self-awareness, coping mechanisms, work-life balance, leadership, and managing uncertainty",
            "domain_number": 8
        }
    }

    # Create parent category items (depth 0)
    for category, info in category_info.items():
        cat_competencies = categories.get(category, [])
        children_ids = [f"{info['id']}/{comp['Concise_Name']}" for comp in cat_competencies]

        item = DimensionItem(
            id=info['id'],
            path_components=[info['id']],
            depth=0,
            parent_id=None,
            children_ids=children_ids,
            name=category,
            description=info['description'],
            level_info={
                0: {
                    "name": category,
                    "level_name": "Domain"
                }
            },
            metadata={
                "domain_number": info['domain_number'],
                "competency_count": len(cat_competencies)
            }
        )
        items.append(item)

    # Create individual task items (depth 1)
    for category, comps in categories.items():
        parent_info = category_info[category]
        parent_id = parent_info['id']

        for comp in comps:
            task_id = f"{parent_id}/{comp['Concise_Name']}"

            item = DimensionItem(
                id=task_id,
                path_components=[parent_id, comp['Concise_Name']],
                depth=1,
                parent_id=parent_id,
                children_ids=[],
                name=comp['Concise_Name'].replace('-', ' ').title(),
                description=comp['Competency'],
                level_info={
                    0: {
                        "name": category,
                        "level_name": "Domain"
                    },
                    1: {
                        "name": comp['Concise_Name'].replace('-', ' ').title(),
                        "level_name": "Competency"
                    }
                },
                metadata={
                    "competency_id": comp['ID'],
                    "concise_name": comp['Concise_Name'],
                    "ai_interaction_mode": comp['AI_Interaction_Mode'],
                    "medhelm_category": comp['MedHELM_Category'],
                    "domain": category
                }
            )
            items.append(item)

    return items

def generate_task_dimension():
    """Generate the complete task dimension"""

    items = create_task_items()

    dimension = SkillMixDimension(
        dimension=DimensionType.CARE_TASK,
        description="Cognitive tasks that intelligent systems aim to augment or automate. Anchored in actual cognitive work physicians perform for principled decisions about automation versus augmentation. Based on the Physician Competency Reference Set synthesizing 150+ competency frameworks.",
        reference=ReferenceInfo(
            classification="Physician Competency Reference Set (Englander et al.)",
            burden_metric="Clinical competency requirements across 8 domains",
            data_source="Physician competency frameworks synthesized from 150+ competency lists",
            last_updated="2025-01-30",
            sources=[
                "Physician Competency Reference Set: 58 competencies across 8 domains (Englander et al.)",
                "MedHELM Framework: 121 medical tasks in 5 categories for LLM evaluation",
                "Eight Domains: Patient Care, Knowledge for Practice, Practice-Based Learning, Communication, Professionalism, Systems-Based Practice, Interprofessional Collaboration, Personal Development",
                "AI Interaction Modes: Augmentation, Automation, Collaborative, Human-Essential"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Eight competency domains with specific cognitive tasks categorized by AI interaction modes and MedHELM framework",
            levels=["domain", "competency"],
            max_depth=1
        ),
        items=items,
        dimension_metadata={
            "total_competencies": 58,
            "total_domains": 8,
            "ai_interaction_modes": ["Augmentation", "Automation", "Collaborative", "Human-Essential"],
            "medhelm_categories": [
                "Clinical Decision Support",
                "Documentation & Note Generation",
                "Patient Communication & Education",
                "Knowledge Synthesis & Research",
                "Administrative & Workflow",
                "Professional Development"
            ]
        }
    )

    return dimension

def save_dimension(dimension):
    """Save the task dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'care_task.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated care_task.json with {len(dimension.items)} care tasks")
    print(f"  - 8 domains (depth 0)")
    print(f"  - 58 competencies (depth 1)")
    print(f"✓ Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating cognitive task dimension...")
    print("=" * 60)

    try:
        dimension = generate_task_dimension()
        output_path = save_dimension(dimension)

        print("=" * 60)
        print("✓ Task dimension generation complete!")
        print(f"\nDomains included:")
        domains = [item for item in dimension.items if item.depth == 0]
        for item in domains:
            comp_count = item.metadata.get('competency_count', 0)
            print(f"  - {item.name}: {comp_count} competencies")

        print(f"\nAI Interaction Modes integrated:")
        for mode in dimension.dimension_metadata['ai_interaction_modes']:
            print(f"  - {mode}")

        print(f"\nMedHELM Categories integrated:")
        for category in dimension.dimension_metadata['medhelm_categories']:
            print(f"  - {category}")

    except Exception as e:
        print(f"❌ Error generating task.json: {e}")
        import traceback
        traceback.print_exc()
        raise
