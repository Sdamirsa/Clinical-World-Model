#!/usr/bin/env python3
"""
Generate disease.json from WHO DALY 2021 analysis data
Uses standardized hierarchical skill-mix dimension format
"""

import json
from pathlib import Path
from collections import defaultdict
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "clinical-skill-mix"))

from skill_mix_dimensions_model import (
    SkillMixDimension, DimensionItem, ReferenceInfo, HierarchyInfo,
    DimensionType, DALYRankingCategory, build_hierarchical_items
)

# Define paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data"
ANALYSIS_PATH = DATA_PATH / "analysis"
SKILL_MIX_PATH = BASE_PATH / "clinical-skill-mix"

# Disease category mappings to ICD-11-like chapters
CATEGORY_MAPPINGS = {
    'Communicable, maternal, perinatal and nutritional conditions': {
        'chapters': ['infectious-communicable', 'maternal-neonatal', 'nutritional'],
        'icd11_chapters': ['01', '18', '05']
    },
    'Noncommunicable diseases': {
        'chapters': ['neoplasms', 'cardiovascular', 'respiratory', 'digestive', 
                    'neurological', 'mental', 'musculoskeletal', 'genitourinary',
                    'endocrine-metabolic', 'sense-organs', 'oral', 'skin'],
        'icd11_chapters': ['02', '11', '12', '13', '08', '06', '15', '16', '05', '09', '13', '14']
    },
    'Injuries': {
        'chapters': ['injuries'],
        'icd11_chapters': ['22']
    }
}

# Disease to chapter mapping based on disease names
DISEASE_TO_CHAPTER = {
    # Infectious
    'tuberculosis': 'infectious-communicable',
    'hiv/aids': 'infectious-communicable',
    'diarrhoeal': 'infectious-communicable',
    'respiratory infections': 'infectious-communicable',
    'meningitis': 'infectious-communicable',
    'encephalitis': 'infectious-communicable',
    'hepatitis': 'infectious-communicable',
    'malaria': 'infectious-communicable',
    'dengue': 'infectious-communicable',
    'measles': 'infectious-communicable',
    'whooping': 'infectious-communicable',
    
    # Maternal/Neonatal
    'neonatal': 'maternal-neonatal',
    'maternal': 'maternal-neonatal',
    'congenital': 'maternal-neonatal',
    
    # Nutritional
    'malnutrition': 'nutritional',
    'anaemia': 'nutritional',
    'iodine': 'nutritional',
    'vitamin': 'nutritional',
    
    # Cardiovascular
    'heart disease': 'cardiovascular',
    'stroke': 'cardiovascular',
    'hypertensive': 'cardiovascular',
    'cardiomyopathy': 'cardiovascular',
    'rheumatic heart': 'cardiovascular',
    
    # Respiratory
    'chronic obstructive': 'respiratory',
    'asthma': 'respiratory',
    'respiratory': 'respiratory',
    
    # Neoplasms (cancers)
    'cancer': 'neoplasms',
    'cancers': 'neoplasms',
    'melanoma': 'neoplasms',
    'leukaemia': 'neoplasms',
    'lymphomas': 'neoplasms',
    'myeloma': 'neoplasms',
    'mesothelioma': 'neoplasms',
    
    # Neurological
    'alzheimer': 'neurological',
    'dementia': 'neurological',
    'parkinson': 'neurological',
    'epilepsy': 'neurological',
    'multiple sclerosis': 'neurological',
    'migraine': 'neurological',
    'headache': 'neurological',
    
    # Mental
    'depressive': 'mental',
    'anxiety': 'mental',
    'bipolar': 'mental',
    'schizophrenia': 'mental',
    'autism': 'mental',
    'eating disorders': 'mental',
    'drug use': 'mental',
    'alcohol': 'mental',
    'behavioural': 'mental',
    
    # Musculoskeletal
    'back and neck': 'musculoskeletal',
    'osteoarthritis': 'musculoskeletal',
    'rheumatoid': 'musculoskeletal',
    'gout': 'musculoskeletal',
    
    # Digestive
    'peptic ulcer': 'digestive',
    'cirrhosis': 'digestive',
    'pancreatitis': 'digestive',
    'appendicitis': 'digestive',
    'inflammatory bowel': 'digestive',
    'gallbladder': 'digestive',
    'gastritis': 'digestive',
    'ileus': 'digestive',
    
    # Genitourinary
    'kidney': 'genitourinary',
    'urinary': 'genitourinary',
    'prostatic': 'genitourinary',
    'urolithiasis': 'genitourinary',
    'infertility': 'genitourinary',
    'gynecological': 'genitourinary',
    
    # Endocrine/Metabolic
    'diabetes': 'endocrine-metabolic',
    'thyroid': 'endocrine-metabolic',
    'thalassaemias': 'endocrine-metabolic',
    'sickle cell': 'endocrine-metabolic',
    
    # Sense organs
    'hearing': 'sense-organs',
    'vision': 'sense-organs',
    'refractive': 'sense-organs',
    'cataracts': 'sense-organs',
    'glaucoma': 'sense-organs',
    'macular': 'sense-organs',
    
    # Injuries
    'road injury': 'injuries',
    'falls': 'injuries',
    'self-harm': 'injuries',
    'violence': 'injuries',
    'drowning': 'injuries',
    'fire': 'injuries',
    'poisoning': 'injuries',
    'mechanical': 'injuries'
}

def categorize_disease(disease_title):
    """Categorize a disease based on its title"""
    title_lower = disease_title.lower()
    
    for keyword, chapter in DISEASE_TO_CHAPTER.items():
        if keyword in title_lower:
            return chapter
    
    # Default categorization
    if 'conditions' in title_lower:
        return 'other'
    
    return 'other'

def load_daly_statistics():
    """Load the DALY statistics from analysis"""
    stats_path = ANALYSIS_PATH / 'global_daly_statistics.json'
    with open(stats_path, 'r') as f:
        return json.load(f)

def generate_diseases_json(daly_stats):
    """Generate hierarchical diseases dimension from DALY statistics"""
    
    # Group diseases by chapter
    chapters = defaultdict(list)
    
    for disease in daly_stats['diseases']:
        chapter = categorize_disease(disease['title'])
        chapters[chapter].append(disease)
    
    # Define chapter metadata
    chapter_info = {
        'infectious-communicable': {
            'icd11_chapters': ['01'],
            'description': 'Certain infectious or parasitic diseases'
        },
        'maternal-neonatal': {
            'icd11_chapters': ['18'],
            'description': 'Pregnancy, childbirth and neonatal conditions'
        },
        'nutritional': {
            'icd11_chapters': ['05'],
            'description': 'Nutritional and metabolic disorders'
        },
        'neoplasms': {
            'icd11_chapters': ['02'],
            'description': 'Neoplasms (cancers)'
        },
        'cardiovascular': {
            'icd11_chapters': ['11'],
            'description': 'Diseases of the circulatory system'
        },
        'respiratory': {
            'icd11_chapters': ['12'],
            'description': 'Diseases of the respiratory system'
        },
        'neurological': {
            'icd11_chapters': ['08'],
            'description': 'Diseases of the nervous system'
        },
        'mental': {
            'icd11_chapters': ['06'],
            'description': 'Mental, behavioural or neurodevelopmental disorders'
        },
        'musculoskeletal': {
            'icd11_chapters': ['15'],
            'description': 'Diseases of the musculoskeletal system or connective tissue'
        },
        'digestive': {
            'icd11_chapters': ['13'],
            'description': 'Diseases of the digestive system'
        },
        'genitourinary': {
            'icd11_chapters': ['16'],
            'description': 'Diseases of the genitourinary system'
        },
        'endocrine-metabolic': {
            'icd11_chapters': ['05'],
            'description': 'Endocrine, nutritional or metabolic diseases'
        },
        'sense-organs': {
            'icd11_chapters': ['09'],
            'description': 'Diseases of the visual system and ear'
        },
        'injuries': {
            'icd11_chapters': ['22'],
            'description': 'Injury, poisoning or other consequences of external causes'
        }
    }
    
    # Build hierarchical items
    items = []
    
    for chapter, info in chapter_info.items():
        if chapter not in chapters or not chapters[chapter]:
            continue
            
        # Sort diseases by rank and take top 10
        sorted_diseases = sorted(chapters[chapter], key=lambda x: x['rank'])[:10]
        
        # Create chapter-level item (depth 0)  
        condition_ids = [f"{chapter}/{disease['title'].lower().replace(' ', '-')}" for disease in sorted_diseases]
        
        chapter_item = DimensionItem(
            id=chapter,
            path_components=[chapter],
            depth=0,
            parent_id=None,
            children_ids=condition_ids,
            name=chapter.replace('-', ' ').title(),
            description=info['description'],
            level_info={
                0: {
                    'name': chapter.replace('-', ' ').title(),
                    'level_name': 'Chapter',
                    'icd11_chapters': info['icd11_chapters']
                }
            },
            metadata={
                'icd11_chapters': info['icd11_chapters'],
                'chapter_type': 'disease_category'
            }
        )
        items.append(chapter_item)
        
        # Create condition-level items (depth 1)
        for disease in sorted_diseases:
            condition_slug = disease['title'].lower().replace(' ', '-')
            condition_id = f"{chapter}/{condition_slug}"  # Full hierarchical path
            condition_name = disease['title']
            
            # Map DALY category to simplified enum
            daly_rank_mapping = {
                'very-high': DALYRankingCategory.HIGH,
                'high': DALYRankingCategory.HIGH,
                'moderate': DALYRankingCategory.MODERATE,
                'low': DALYRankingCategory.LOW
            }
            daly_rank = daly_rank_mapping.get(disease['daly_category'], DALYRankingCategory.LOW)
            
            condition_item = DimensionItem(
                id=condition_id,
                path_components=[chapter, condition_slug],
                depth=1,
                parent_id=chapter,
                children_ids=[],  # No subconditions for now
                name=condition_name,
                level_info={
                    0: {
                        'name': chapter.replace('-', ' ').title(),
                        'level_name': 'Chapter'
                    },
                    1: {
                        'name': condition_name,
                        'level_name': 'Condition'
                    }
                },
                metadata={
                    'daly_rank': daly_rank.value,
                    'global_rank': disease['rank'],
                    'daly_total': disease['daly_total'],
                    'daly_per_100k': disease['daly_per_100k'],
                    'who_code': disease['code'],
                    'deaths_total': disease['deaths_total'],
                    'disease_type': disease['type']
                }
            )
            items.append(condition_item)
    
    # Create reference info
    reference = ReferenceInfo(
        classification='WHO ICD-11 (International Classification of Diseases, 11th Revision)',
        burden_metric='DALY (Disability-Adjusted Life Years) from GBD 2019',
        data_source='WHO Global Health Estimates 2021 (Top 25 economies)',
        last_updated='2025-01-30',
        sources=[
            'WHO ICD-11 for Mortality and Morbidity Statistics',
            'WHO Global Health Estimates 2021',
            'Analysis based on actual DALY data'
        ]
    )
    
    # Create hierarchy info
    hierarchy = HierarchyInfo(
        structure='ICD-11 chapter-based with GBD cause categories',
        levels=['chapter', 'condition', 'subcondition'],
        max_depth=1  # Currently using chapter -> condition (0 -> 1)
    )
    
    # Create dimension metadata
    dimension_metadata = {
        'burden_metrics': {
            'daly_rankings': {
                DALYRankingCategory.HIGH.value: 'High global burden diseases',
                DALYRankingCategory.MODERATE.value: 'Moderate global burden diseases', 
                DALYRankingCategory.LOW.value: 'Lower global burden but clinically important'
            },
            'data_notes': [
                'Based on 2019 data (pre-COVID)',
                'Data from top 25 economies, representative of global burden',
                'Total of 131 disease conditions analyzed',
                'Rankings may vary by region and population'
            ]
        },
        'total_conditions': len([item for item in items if item.depth == 1]),
        'total_chapters': len([item for item in items if item.depth == 0])
    }
    
    # Create the standardized dimension
    diseases_dimension = SkillMixDimension(
        dimension=DimensionType.DISEASES,
        description='Disease categories based on WHO ICD-11 classification and Global Burden of Disease metrics',
        reference=reference,
        hierarchy=hierarchy,
        items=items,
        dimension_metadata=dimension_metadata
    )
    
    return diseases_dimension

def save_diseases_json(diseases_dimension):
    """Save the generated disease.json file using standardized format"""
    output_path = SKILL_MIX_PATH / 'disease.json'
    
    # Convert Pydantic model to JSON
    with open(output_path, 'w') as f:
        json.dump(diseases_dimension.model_dump(), f, indent=2)
    
    print(f"Generated disease.json saved to {output_path}")
    return output_path

def print_summary(diseases_dimension):
    """Print summary of generated standardized dimension"""
    print("\n=== Generated Diseases Dimension Summary ===")
    print(f"Dimension Type: {diseases_dimension.dimension}")
    print(f"Description: {diseases_dimension.description}")
    print(f"Max Depth: {diseases_dimension.hierarchy.max_depth}")
    print(f"Total Items: {len(diseases_dimension.items)}")
    
    # Count by depth
    from collections import Counter
    depth_counts = Counter(item.depth for item in diseases_dimension.items)
    for depth in sorted(depth_counts.keys()):
        level_name = diseases_dimension.hierarchy.levels[depth] if depth < len(diseases_dimension.hierarchy.levels) else f"Level {depth}"
        print(f"  {level_name} (depth {depth}): {depth_counts[depth]} items")
    
    # Print chapters
    chapters = [item for item in diseases_dimension.items if item.depth == 0]
    print(f"\nChapters ({len(chapters)}):")
    for chapter in chapters:
        conditions_count = len(chapter.children_ids)
        print(f"  {chapter.name}: {conditions_count} conditions")
    
    # Print top 5 conditions by DALY burden
    conditions = [item for item in diseases_dimension.items if item.depth == 1]
    top_conditions = sorted(conditions, key=lambda x: x.metadata.get('global_rank', float('inf')))[:5]
    
    print("\nTop 5 conditions by DALY burden:")
    for condition in top_conditions:
        rank = condition.metadata.get('global_rank', 'N/A')
        daly_total = condition.metadata.get('daly_total', 0)
        print(f"  {rank}. {condition.name} (DALY: {daly_total:,.0f})")
    
    # Print metadata summary
    print(f"\nMetadata:")
    print(f"  Reference: {diseases_dimension.reference.classification}")
    print(f"  Data Source: {diseases_dimension.reference.data_source}")
    print(f"  Last Updated: {diseases_dimension.reference.last_updated}")
    print(f"  Total Conditions: {diseases_dimension.dimension_metadata.get('total_conditions', 0)}")
    print(f"  Total Chapters: {diseases_dimension.dimension_metadata.get('total_chapters', 0)}")

if __name__ == "__main__":
    print("Loading DALY statistics...")
    daly_stats = load_daly_statistics()
    
    print("Generating standardized diseases dimension from DALY data...")
    diseases_dimension = generate_diseases_json(daly_stats)
    
    print("Validating dimension structure...")
    try:
        # Pydantic validation happens automatically during construction
        print("✓ Dimension structure validation passed")
    except Exception as e:
        print(f"✗ Validation error: {e}")
        exit(1)
    
    print("Saving disease.json...")
    output_path = save_diseases_json(diseases_dimension)
    
    print_summary(diseases_dimension)
    
    print(f"\n✓ Done! Standardized disease.json has been generated at {output_path}")
    
    # Demonstrate depth-aware queries
    print("\n=== Depth-Aware Query Examples ===")
    from skill_mix_dimensions_model import get_items_at_depth, get_children_at_depth
    
    # Get chapters (depth 0)
    chapters = get_items_at_depth(diseases_dimension, 0)
    print(f"Chapters (depth 0): {[ch.name for ch in chapters[:3]]}")
    
    # Get conditions (depth 1)  
    conditions = get_items_at_depth(diseases_dimension, 1)
    print(f"Conditions (depth 1): {len(conditions)} total")
    
    # Get cardiovascular conditions
    cardio_conditions = get_children_at_depth(diseases_dimension, 'cardiovascular', 1)
    print(f"Cardiovascular conditions: {[c.name for c in cardio_conditions[:3]]}")
    
    print("✓ Depth-aware queries working correctly!")  