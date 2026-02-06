#!/usr/bin/env python3
"""
Generate conditions.json from ICD-10-CM major codes (Code Length = 3, Header = 0)
Replaces the previous GBD-based generation with ICD-10-CM classification
"""

import json
import csv
from pathlib import Path
import sys
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "clinical-skill-mix"))

from skill_mix_dimensions_model import (
    SkillMixDimension, DimensionItem, ReferenceInfo, HierarchyInfo, DimensionType
)

# Define paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data"
SKILL_MIX_PATH = BASE_PATH / "clinical-skill-mix"
ICD10_CSV = DATA_PATH / "ICD10CM-PCS.csv"

# ICD-10-CM Chapter mapping (based on code letter prefixes)
ICD10_CHAPTERS = {
    'A': 'Infectious and parasitic diseases',
    'B': 'Infectious and parasitic diseases',
    'C': 'Neoplasms',
    'D': 'Diseases of blood and certain disorders involving immune mechanism / Neoplasms',
    'E': 'Endocrine, nutritional and metabolic diseases',
    'F': 'Mental, behavioral and neurodevelopmental disorders',
    'G': 'Diseases of the nervous system',
    'H': 'Diseases of the eye and adnexa / Diseases of the ear and mastoid process',
    'I': 'Diseases of the circulatory system',
    'J': 'Diseases of the respiratory system',
    'K': 'Diseases of the digestive system',
    'L': 'Diseases of the skin and subcutaneous tissue',
    'M': 'Diseases of the musculoskeletal system and connective tissue',
    'N': 'Diseases of the genitourinary system',
    'O': 'Pregnancy, childbirth and the puerperium',
    'P': 'Certain conditions originating in the perinatal period',
    'Q': 'Congenital malformations, deformations and chromosomal abnormalities',
    'R': 'Symptoms, signs and abnormal clinical and laboratory findings',
    'S': 'Injury, poisoning and certain other consequences of external causes',
    'T': 'Injury, poisoning and certain other consequences of external causes',
    'U': 'Codes for special purposes',
    'V': 'External causes of morbidity',
    'W': 'External causes of morbidity',
    'X': 'External causes of morbidity',
    'Y': 'External causes of morbidity',
    'Z': 'Factors influencing health status and contact with health services'
}

def parse_icd10_csv():
    """Parse ICD-10-CM CSV and extract major codes (Code Length = 3, Header = 0)"""
    conditions = []

    with open(ICD10_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code_length = int(row['Code Length'])
            header_flag = int(row['header_0 or transaction_1'])

            # Filter: Code Length = 3 (include both Header = 0 and Header = 1 for complete coverage)
            if code_length == 3:
                code = row['Code'].strip()
                short_desc = row['Short description'].strip()
                long_desc = row['Long description'].strip()

                # Use long description if available, otherwise short description
                description = long_desc if long_desc else short_desc

                conditions.append({
                    'code': code,
                    'name': description,
                    'chapter_letter': code[0]  # First character indicates chapter
                })

    print(f"Parsed {len(conditions)} ICD-10-CM major codes from CSV")
    return conditions

def group_by_chapter(conditions):
    """Group conditions by ICD-10-CM chapter"""
    chapters = defaultdict(list)

    for condition in conditions:
        letter = condition['chapter_letter']
        chapter_name = ICD10_CHAPTERS.get(letter, f'Chapter {letter}')
        chapters[letter].append(condition)

    return chapters

def create_dimension_items(conditions):
    """Create hierarchical dimension items: Chapter -> Condition"""
    chapters_dict = group_by_chapter(conditions)
    items = []

    # Create chapter-level items (depth 0)
    for letter in sorted(chapters_dict.keys()):
        chapter_name = ICD10_CHAPTERS.get(letter, f'Chapter {letter}')
        chapter_id = f'chapter-{letter.lower()}'

        # Get all condition codes for this chapter
        chapter_conditions = chapters_dict[letter]
        children_ids = [f"{chapter_id}/{cond['code'].lower()}" for cond in chapter_conditions]

        chapter_item = DimensionItem(
            id=chapter_id,
            path_components=[chapter_id],
            depth=0,
            parent_id=None,
            children_ids=children_ids,
            name=chapter_name,
            description=f"ICD-10-CM Chapter {letter}: {chapter_name}",
            level_info={
                0: {
                    "name": chapter_name,
                    "level_name": "Chapter"
                }
            },
            metadata={
                "chapter_letter": letter,
                "condition_count": len(chapter_conditions)
            }
        )
        items.append(chapter_item)

        # Create condition-level items (depth 1)
        for condition in chapter_conditions:
            condition_id = f"{chapter_id}/{condition['code'].lower()}"

            condition_item = DimensionItem(
                id=condition_id,
                path_components=[chapter_id, condition['code'].lower()],
                depth=1,
                parent_id=chapter_id,
                children_ids=[],
                name=condition['name'],
                description=f"{condition['code']}: {condition['name']}",
                level_info={
                    0: {
                        "name": chapter_name,
                        "level_name": "Chapter"
                    },
                    1: {
                        "name": condition['name'],
                        "level_name": "ICD-10-CM Code"
                    }
                },
                metadata={
                    "icd10_code": condition['code'],
                    "chapter": chapter_name
                }
            )
            items.append(condition_item)

    return items

def generate_conditions_dimension():
    """Generate the complete conditions dimension from ICD-10-CM"""

    # Parse CSV
    conditions = parse_icd10_csv()

    # Create dimension items
    items = create_dimension_items(conditions)

    # Create dimension
    dimension = SkillMixDimension(
        dimension=DimensionType.CONDITION,
        description="Medical conditions classified according to ICD-10-CM (International Classification of Diseases, 10th Revision, Clinical Modification). This dimension uses ALL 3-character codes including both category headers (with sub-codes) and standalone diagnostic codes for complete clinical coverage across all medical specialties.",
        reference=ReferenceInfo(
            classification="ICD-10-CM (International Classification of Diseases, 10th Revision, Clinical Modification)",
            burden_metric="Clinical prevalence and healthcare system utilization",
            data_source="ICD-10-CM official classification",
            last_updated="2026-02-05",
            sources=[
                "ICD-10-CM official coding guidelines",
                "Centers for Medicare & Medicaid Services (CMS)",
                "World Health Organization ICD-10 base classification",
                "National Center for Health Statistics (NCHS)"
            ]
        ),
        hierarchy=HierarchyInfo(
            structure="Two-level hierarchy: ICD-10-CM Chapter (letter-based) → Major Category Code (3-character)",
            levels=["chapter", "code"],
            max_depth=1
        ),
        items=items
    )

    return dimension

def save_dimension(dimension):
    """Save the conditions dimension to JSON file"""
    output_path = SKILL_MIX_PATH / 'conditions.json'

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension.dict(), f, indent=2, ensure_ascii=False)

    print(f"Generated conditions.json with {len(dimension.items)} items")
    print(f"Saved to {output_path}")

    return output_path

if __name__ == "__main__":
    print("Generating conditions dimension from ICD-10-CM major codes...")
    print("=" * 70)

    try:
        # Check if CSV exists
        if not ICD10_CSV.exists():
            print(f"ERROR: ICD-10-CM CSV not found at {ICD10_CSV}")
            sys.exit(1)

        # Generate dimension
        dimension = generate_conditions_dimension()

        # Save to file
        output_path = save_dimension(dimension)

        print("=" * 70)
        print("Conditions dimension generation complete!")
        print(f"\nStatistics:")

        # Count chapters and conditions
        chapters = [item for item in dimension.items if item.depth == 0]
        conditions = [item for item in dimension.items if item.depth == 1]

        print(f"  Chapters: {len(chapters)}")
        print(f"  Major category codes: {len(conditions)}")
        print(f"  Total items: {len(dimension.items)}")

        # Show first few chapters
        print(f"\nFirst 5 chapters:")
        for chapter in chapters[:5]:
            print(f"  - {chapter.name} ({chapter.metadata.get('condition_count', 0)} codes)")

    except Exception as e:
        print(f"ERROR: Failed to generate conditions.json: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
