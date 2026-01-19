#!/usr/bin/env python3
"""
Generate persona.json from WHO health worker classification data.

This script processes WHO CSV files to create a comprehensive personas dimension
following the standardized Pydantic format for clinical skill-mix dimensions.

Data Sources:
- WHO_health_worker_classification.csv: Main occupational categories with ISCO codes
- WHO_health_worker_classification_specialities.csv: Medical specialties for specialists

Structure:
- Level 0: WHO occupational groups (e.g., Generalist medical practitioners, Nursing professionals)
- Level 1: Medical specialties for Specialist medical practitioners (e.g., Cardiology, Surgery)
- Level 2: Not implemented in this WHO-based approach

Author: Clinical World Model Framework
Date: 2025-01-30
"""

import pandas as pd
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import re


def normalize_id(text: str) -> str:
    """
    Convert text to standardized ID format (lowercase, hyphenated).
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized ID string
    """
    # Remove parenthetical content and extra whitespace
    text = re.sub(r'\([^)]*\)', '', text).strip()
    # Convert to lowercase and replace spaces/special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def create_dimension_item(
    id_str: str,
    path_components: List[str],
    depth: int,
    parent_id: Optional[str],
    children_ids: List[str],
    name: str,
    description: str,
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a standardized dimension item following the Pydantic model.
    
    Args:
        id_str: Unique identifier for the item
        path_components: Hierarchical path components
        depth: Hierarchy level (0, 1, 2...)
        parent_id: Parent item ID (None for root level)
        children_ids: List of child item IDs
        name: Display name
        description: Detailed description
        metadata: Dimension-specific metadata
        
    Returns:
        Formatted dimension item dictionary
    """
    # Create level_info dynamically based on depth
    level_info = {}
    level_names = ["Role", "Specialty", "Subspecialty"]
    
    for i in range(depth + 1):
        level_info[str(i)] = {
            "name": path_components[i].replace('-', ' ').title(),
            "level_name": level_names[min(i, len(level_names) - 1)]
        }
    
    return {
        "id": id_str,
        "path_components": path_components,
        "depth": depth,
        "parent_id": parent_id,
        "children_ids": children_ids,
        "name": name,
        "description": description,
        "level_info": level_info,
        "metadata": metadata
    }


def load_and_process_classification_data(csv_path: str) -> pd.DataFrame:
    """
    Load and process WHO health worker classification data.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Processed DataFrame
    """
    try:
        # Try different encodings to handle various file formats
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                print(f"Successfully loaded {csv_path} with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise Exception("Could not decode file with any supported encoding")
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        # Fill empty cells with empty strings for consistent processing
        df = df.fillna('')
        
        return df
    
    except Exception as e:
        print(f"Error loading {csv_path}: {e}")
        return pd.DataFrame()


def extract_examples_list(examples_text: str) -> List[str]:
    """
    Extract and clean examples from semicolon-separated text.
    
    Args:
        examples_text: Raw examples text
        
    Returns:
        List of cleaned example strings
    """
    if not examples_text or pd.isna(examples_text):
        return []
    
    examples = [ex.strip() for ex in str(examples_text).split(';') if ex.strip()]
    return examples[:10]  # Limit to first 10 examples to avoid excessive data


def create_metadata_for_occupation(row: pd.Series) -> Dict[str, Any]:
    """
    Create comprehensive metadata for an occupation from WHO data.
    
    Args:
        row: DataFrame row containing occupation data
        
    Returns:
        Metadata dictionary
    """
    metadata = {
        "isco_code": str(row.get('ISCO code', '')).strip(),
        "who_classification": True,
        "occupation_type": "health_worker"
    }
    
    # Add examples if available
    examples = extract_examples_list(row.get('Examples', ''))
    if examples:
        metadata["occupation_examples"] = examples
    
    # Add notes if available
    notes = str(row.get('Notes', '')).strip()
    if notes and notes != 'nan':
        metadata["training_notes"] = notes
    
    # Determine scope based on occupation group
    occupation_group = str(row.get('Occupation group', '')).lower()
    
    if 'medical practitioner' in occupation_group:
        metadata["scope"] = "medical_practice"
        metadata["prescriptive_authority"] = True
        metadata["independent_practice"] = True
    elif 'nursing' in occupation_group:
        metadata["scope"] = "nursing_care"
        metadata["prescriptive_authority"] = False  # Generally, though varies by jurisdiction
        metadata["independent_practice"] = "varies"
    elif 'dental' in occupation_group:
        metadata["scope"] = "oral_health"
        metadata["prescriptive_authority"] = "limited"
        metadata["independent_practice"] = True
    elif 'technician' in occupation_group or 'assistant' in occupation_group:
        metadata["scope"] = "technical_support"
        metadata["prescriptive_authority"] = False
        metadata["supervision_required"] = True
    elif 'manager' in occupation_group:
        metadata["scope"] = "health_administration"
        metadata["management_role"] = True
    else:
        metadata["scope"] = "health_services"
    
    return metadata


def process_specialties_data(specialties_csv_path: str) -> Dict[str, List[str]]:
    """
    Process medical specialties data and group by specialty groups.
    
    Args:
        specialties_csv_path: Path to specialties CSV file
        
    Returns:
        Dictionary mapping specialty groups to lists of specialties
    """
    df = load_and_process_classification_data(specialties_csv_path)
    
    if df.empty:
        print("Warning: Specialties data is empty")
        return {}
    
    specialty_groups = {}
    
    for _, row in df.iterrows():
        group = str(row.get('Specialty Group', '')).strip()
        specialty = str(row.get('Speciality', '')).strip()
        
        if group and specialty and group != 'nan' and specialty != 'nan':
            if group not in specialty_groups:
                specialty_groups[group] = []
            specialty_groups[group].append(specialty)
    
    return specialty_groups


def generate_personas_json(
    classification_csv_path: str,
    specialties_csv_path: str,
    output_path: str
) -> None:
    """
    Generate comprehensive persona.json from WHO data.
    
    Args:
        classification_csv_path: Path to main classification CSV
        specialties_csv_path: Path to specialties CSV
        output_path: Output path for generated JSON
    """
    print("Loading WHO health worker classification data...")
    
    # Load main classification data
    df_classification = load_and_process_classification_data(classification_csv_path)
    
    if df_classification.empty:
        print("Error: No classification data found")
        return
    
    # Load specialties data
    specialty_groups = process_specialties_data(specialties_csv_path)
    
    # Initialize the dimension structure
    dimension_data = {
        "dimension": "personas",
        "description": "Healthcare provider roles based on WHO health worker classification with ISCO codes",
        "reference": {
            "classification": "WHO Health Worker Classification and ISCO-08 Standards",
            "burden_metric": "Professional scope, training requirements, and regulatory status",
            "data_source": "World Health Organization Health Worker Classification and International Standard Classification of Occupations",
            "last_updated": "2025-01-30",
            "sources": [
                "WHO Health Worker Classification Framework",
                "International Standard Classification of Occupations (ISCO-08)",
                "Medical specialty classification systems",
                "Professional health worker regulatory standards"
            ]
        },
        "hierarchy": {
            "structure": "Healthcare occupations with medical specializations",
            "levels": ["occupation", "specialty"],
            "max_depth": 1  # Level 0: occupation groups, Level 1: specialties for medical practitioners
        },
        "items": [],
        "dimension_metadata": {}
    }
    
    # Track items and relationships
    all_items = []
    specialist_medical_practitioners_id = None
    
    print(f"Processing {len(df_classification)} occupation groups...")
    
    # Process each occupation group (Level 0)
    for _, row in df_classification.iterrows():
        occupation_group = str(row.get('Occupation group', '')).strip()
        
        if not occupation_group or occupation_group == 'nan':
            continue
        
        # Create normalized ID
        occupation_id = normalize_id(occupation_group)
        
        # Skip duplicates or invalid entries
        if any(item['id'] == occupation_id for item in all_items):
            continue
        
        # Determine if we'll add specialties for this occupation
        children_ids = []
        if occupation_group.lower() == 'specialist medical practitioners':
            specialist_medical_practitioners_id = occupation_id
        
        # Create metadata
        metadata = create_metadata_for_occupation(row)
        
        # Create the occupation item
        occupation_item = create_dimension_item(
            id_str=occupation_id,
            path_components=[occupation_id],
            depth=0,
            parent_id=None,
            children_ids=children_ids,  # Will be updated later
            name=occupation_group,
            description=str(row.get('Definition', '')).strip(),
            metadata=metadata
        )
        
        all_items.append(occupation_item)
    
    print(f"Processed {len(all_items)} occupation groups")
    
    # Process medical specialties (Level 1) for Specialist medical practitioners
    if specialist_medical_practitioners_id and specialty_groups:
        print(f"Adding {sum(len(specs) for specs in specialty_groups.values())} medical specialties...")
        
        specialist_children = []
        
        for specialty_group, specialties in specialty_groups.items():
            for specialty in specialties:
                if not specialty or specialty.lower() == 'nan':
                    continue
                
                specialty_id = f"{specialist_medical_practitioners_id}/{normalize_id(specialty)}"
                specialist_children.append(specialty_id)
                
                # Create metadata for specialty
                specialty_metadata = {
                    "specialty_group": specialty_group,
                    "medical_specialty": True,
                    "who_classification": True,
                    "requires_specialization": True,
                    "postgraduate_training": True,
                    "board_certification": "varies_by_jurisdiction"
                }
                
                # Add specific metadata based on specialty type
                specialty_lower = specialty.lower()
                if any(term in specialty_lower for term in ['surgery', 'surgical']):
                    specialty_metadata["specialty_type"] = "surgical"
                    specialty_metadata["procedural_focus"] = True
                elif any(term in specialty_lower for term in ['psychiatry', 'psychology']):
                    specialty_metadata["specialty_type"] = "mental_health"
                elif any(term in specialty_lower for term in ['pediatrics', 'paediatrics']):
                    specialty_metadata["specialty_type"] = "pediatric"
                    specialty_metadata["patient_population"] = "children"
                elif any(term in specialty_lower for term in ['internal', 'medicine']):
                    specialty_metadata["specialty_type"] = "internal_medicine"
                else:
                    specialty_metadata["specialty_type"] = "medical"
                
                # Create the specialty item
                specialty_item = create_dimension_item(
                    id_str=specialty_id,
                    path_components=[specialist_medical_practitioners_id, normalize_id(specialty)],
                    depth=1,
                    parent_id=specialist_medical_practitioners_id,
                    children_ids=[],
                    name=specialty.title(),
                    description=f"Medical specialist in {specialty.lower()}",
                    metadata=specialty_metadata
                )
                
                all_items.append(specialty_item)
        
        # Update the specialist medical practitioners item with children
        for item in all_items:
            if item['id'] == specialist_medical_practitioners_id:
                item['children_ids'] = sorted(specialist_children)
                break
    
    # Sort items by ID for consistent output
    all_items.sort(key=lambda x: x['id'])
    
    # Add items to dimension data
    dimension_data['items'] = all_items
    
    # Create comprehensive dimension metadata
    occupation_counts = {}
    specialty_counts = 0
    
    for item in all_items:
        if item['depth'] == 0:
            occupation_type = item['metadata'].get('scope', 'other')
            occupation_counts[occupation_type] = occupation_counts.get(occupation_type, 0) + 1
        elif item['depth'] == 1:
            specialty_counts += 1
    
    dimension_data['dimension_metadata'] = {
        "total_occupations": len([item for item in all_items if item['depth'] == 0]),
        "total_specialties": specialty_counts,
        "occupation_distribution": occupation_counts,
        "specialty_groups": len(set(specialty_groups.keys())) if specialty_groups else 0,
        "who_isco_classification": True,
        "evidence_based": True,
        "international_standard": True,
        "last_updated": "2025-01-30"
    }
    
    # Write to file
    print(f"Writing persona.json with {len(all_items)} total items...")
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dimension_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully generated {output_path}")
    print(f"   📊 Total items: {len(all_items)}")
    print(f"   👥 Occupation groups: {len([item for item in all_items if item['depth'] == 0])}")
    print(f"   🩺 Medical specialties: {specialty_counts}")
    print(f"   📁 Specialty groups: {len(set(specialty_groups.keys())) if specialty_groups else 0}")


def main():
    """Main execution function."""
    # Define file paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    output_dir = base_dir / "clinical-skill-mix"
    
    classification_csv = data_dir / "WHO_health_worker_classification.csv"
    specialties_csv = data_dir / "WHO_health_worker_classification_specialities.csv"
    output_json = output_dir / "persona.json"
    
    # Verify input files exist
    if not classification_csv.exists():
        print(f"Error: {classification_csv} not found")
        return
    
    if not specialties_csv.exists():
        print(f"Warning: {specialties_csv} not found - proceeding without specialties")
        specialties_csv = None
    
    # Generate the persona.json file
    try:
        generate_personas_json(
            str(classification_csv),
            str(specialties_csv) if specialties_csv else "",
            str(output_json)
        )
        
        print("\n🎉 Personas dimension generated successfully!")
        print("📋 Next steps:")
        print("   1. Review the generated persona.json file")
        print("   2. Copy to docs/clinical-skill-mix/ for website access")
        print("   3. Test with the interactive website")
        
    except Exception as e:
        print(f"❌ Error generating persona.json: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()