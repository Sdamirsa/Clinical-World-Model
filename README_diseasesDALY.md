# Disease Burden Analysis Using DALY Data

This document explains our approach to analyzing disease burden using Disability-Adjusted Life Years (DALY) data from the World Health Organization (WHO) Global Health Estimates 2021.

## Overview

Our Clinical Skill-Mix framework incorporates evidence-based disease prioritization using real-world burden metrics. Rather than arbitrary disease selection, we use WHO's authoritative DALY data to rank diseases by their global health impact and create a standardized, hierarchical disease dimension.

## Data Source

### WHO Global Health Estimates 2021
- **Coverage**: Top 25 global economies (representing ~70% of global GDP)
- **Temporal**: 2019 baseline data (pre-COVID-19 pandemic)
- **Scope**: 131 distinct disease conditions
- **Demographics**: All age groups, both sexes
- **Format**: Pre-calculated DALY values by WHO methodology

### Dataset Structure
```
Columns: COUNTRY_CODE, COUNTRY, GHE_CAUSE_CODE, GHE_CAUSE_TITLE, GHE_CAUSE_TYPE, 
         YEAR, SEX_CODE, AGEGROUP_CODE, POPULATION, DEATHS, DEATHS_RATE, 
         DEATHS_100K, DALY, DALY_RATE, DALY_100K
```

## DALY Methodology

### What is DALY?
**DALY (Disability-Adjusted Life Years)** is a metric that quantifies the burden of disease by combining:
- **Years of Life Lost (YLL)**: Premature mortality
- **Years Lived with Disability (YLD)**: Morbidity impact

**Formula**: `DALY = YLL + YLD`

### WHO's DALY Calculation
1. **YLL Calculation**:
   - `YLL = Deaths × Standard Life Expectancy at age of death`
   - Uses WHO standard life tables

2. **YLD Calculation**:
   - `YLD = Prevalence × Disability Weight × Average Duration`
   - Disability weights: 0 (perfect health) to 1 (death equivalent)

3. **Additional Considerations**:
   - Age standardization
   - Time discounting (optional)
   - Uncertainty intervals

## Our Analysis Approach

### Data Processing Pipeline

```
WHO Raw Data → Filtering → Aggregation → Ranking → Categorization → Prioritization → Hierarchical Structure
```

### 1. Data Filtering (`analyze_daly_data.py`)
```python
# Filter for 2019 data (pre-COVID baseline)
df_2019 = df[df['YEAR'] == 2019]
```

### 2. Global Aggregation
```python
# Sum across all countries, sexes, and age groups
disease_daly = df_2019.groupby(['GHE_CAUSE_CODE', 'GHE_CAUSE_TITLE', 'GHE_CAUSE_TYPE']).agg({
    'DALY': 'sum',        # Total DALY burden
    'DEATHS': 'sum',      # Total deaths
    'POPULATION': 'sum'   # Total population at risk
}).reset_index()
```

### 3. Rate Calculation
```python
# Calculate burden per 100,000 population
disease_daly['DALY_PER_100K'] = (disease_daly['DALY'] / disease_daly['POPULATION']) * 100000
disease_daly['DEATHS_PER_100K'] = (disease_daly['DEATHS'] / disease_daly['POPULATION']) * 100000
```

### 4. Global Ranking
```python
# Rank diseases by total DALY burden
disease_daly = disease_daly.sort_values('DALY', ascending=False)
disease_daly['GLOBAL_RANK'] = range(1, len(disease_daly) + 1)
```

### 5. Burden Categorization
```python
# Categorize diseases by burden level
disease_daly['DALY_CATEGORY'] = pd.cut(
    disease_daly['GLOBAL_RANK'],
    bins=[0, 10, 30, 50, float('inf')],
    labels=['very-high', 'high', 'moderate', 'low']
)
```

## Disease Prioritization Strategy

### Dual-Level Prioritization Approach
Our approach uses a **two-stage prioritization system** that combines global burden ranking with clinical organization principles:

#### Stage 1: Global DALY Ranking (Evidence-Based)
**Objective**: Rank all 131 diseases by total global DALY burden
```python
# Sort diseases by total DALY burden (descending)
disease_daly = disease_daly.sort_values('DALY', ascending=False)
disease_daly['GLOBAL_RANK'] = range(1, len(disease_daly) + 1)
```

**Result**: Absolute ranking from 1-131 based on quantitative burden
- Rank #1: Ischemic Heart Disease (120.5M DALYs)
- Rank #2: Stroke (94.9M DALYs)  
- Rank #3: Neonatal Conditions (65.5M DALYs)
- etc.

#### Stage 2: Clinical Chapter Organization (Structure-Based)
**Objective**: Group diseases into clinically meaningful categories using ICD-11 structure

**Method**: Keyword-based disease classification
```python
def categorize_disease(disease_title):
    """Categorize disease based on clinical keywords in title"""
    title_lower = disease_title.lower()
    
    # Search for clinical keywords (e.g., 'heart disease' -> 'cardiovascular')
    for keyword, chapter in DISEASE_TO_CHAPTER.items():
        if keyword in title_lower:
            return chapter
    
    return 'other'  # Fallback for unmatched diseases
```

**Keyword Mapping Examples**:
- `'heart disease'` → cardiovascular
- `'cancer'`, `'cancers'` → neoplasms  
- `'tuberculosis'` → infectious-communicable
- `'diabetes'` → endocrine-metabolic
- `'stroke'` → cardiovascular

#### Stage 3: Within-Chapter Prioritization
**Objective**: Select top diseases within each clinical chapter

**Method**: Take top 10 highest-ranked diseases per chapter
```python
for chapter, info in chapter_info.items():
    if chapter in chapters and chapters[chapter]:
        # Sort diseases within chapter by global DALY rank (ascending)
        sorted_diseases = sorted(chapters[chapter], key=lambda x: x['rank'])[:10]
```

**Logic**: 
- Maintains global burden priority within clinical structure
- Ensures each clinical area is represented
- Limits to manageable number per category (10 max)

### Priority Selection Results

#### Chapter Coverage Analysis
```
Chapter                    | Diseases | Top Disease (Global Rank)
---------------------------|----------|-------------------------
Cardiovascular            | 5        | Ischemic Heart Disease (#1)
Respiratory               | 2        | COPD (#4) 
Infectious-Communicable   | 10       | Tuberculosis (#9)
Neoplasms                 | 10       | Lung Cancer (#7)
Mental                    | 9        | Depression (#12)
Musculoskeletal          | 4        | Back/Neck Pain (#8)
Neurological             | 6        | Alzheimer's (#18)
Injuries                 | 9        | Road Injuries (#6)
```

### Prioritization Logic Validation

#### ✅ **Strengths of Our Approach**

1. **Evidence-Based Foundation**: Uses objective DALY burden data
2. **Clinical Relevance**: Organizes by familiar medical categories  
3. **Balanced Representation**: Ensures coverage across clinical domains
4. **Transparent Methodology**: Clear keyword-based categorization rules
5. **Flexible Structure**: Allows querying at different hierarchy levels

#### ⚠️ **Potential Limitations Identified**

1. **Keyword Dependency**: Classification relies on disease name keywords
   - **Risk**: Diseases with ambiguous names might be miscategorized
   - **Example**: "Other hearing loss" correctly → sense-organs
   - **Mitigation**: Comprehensive keyword dictionary (153 mappings)

2. **Chapter Size Imbalance**: 
   - **Issue**: Some chapters have more high-burden diseases
   - **Example**: Infectious diseases (10 conditions) vs Respiratory (2 conditions)
   - **Impact**: May overrepresent certain clinical areas

3. **Fixed Selection Limit**:
   - **Rule**: Maximum 10 diseases per chapter
   - **Risk**: Might exclude important diseases in high-burden chapters
   - **Example**: Cardiovascular limited to 5 despite having more ranked diseases

4. **Categorization Edge Cases**:
   ```python
   # Potential ambiguity examples:
   "Cardiomyopathy, myocarditis, endocarditis" → cardiovascular ✓
   "Paralytic ileus and intestinal obstruction" → digestive ✓  
   "Iron-deficiency anaemia" → nutritional ✓
   ```

#### 🔧 **Code Logic Assessment**

**Categorization Function Analysis**:
```python
def categorize_disease(disease_title):
    title_lower = disease_title.lower()
    for keyword, chapter in DISEASE_TO_CHAPTER.items():
        if keyword in title_lower:
            return chapter
    return 'other'
```

**Logic Evaluation**:
- ✅ **First-match wins**: Returns first keyword found
- ✅ **Case-insensitive**: Handles various capitalizations  
- ✅ **Fallback handling**: Assigns 'other' to unmatched diseases
- ⚠️ **Order dependency**: Earlier keywords in dict take precedence
- ⚠️ **Substring matching**: Could cause false positives (though none observed)

**Ranking Logic Analysis**:
```python
sorted_diseases = sorted(chapters[chapter], key=lambda x: x['rank'])[:10]
```

- ✅ **Preserves global ranking**: Maintains DALY-based priority within chapters
- ✅ **Consistent selection**: Always takes top N by objective criteria
- ✅ **Prevents bias**: No subjective disease selection

### Validation Results

**Categorization Accuracy Test**:
```
Disease                          | Predicted        | Expected         | ✓/✗
Ischaemic heart disease         | cardiovascular   | cardiovascular   | ✓
Tuberculosis                    | infectious-comm. | infectious-comm. | ✓
Trachea, bronchus, lung cancers | neoplasms       | neoplasms        | ✓
Diabetes mellitus               | endocrine-metab. | endocrine-metab. | ✓
Unknown disease name            | other           | other            | ✓
```

**Chapter Representation Validation**:
- All major disease categories represented ✓
- High-burden diseases properly distributed ✓  
- Clinical logic maintained ✓

## Results Summary

### Top 10 Diseases by Global DALY Burden (2019)

| Rank | Disease | DALY (Millions) | Type |
|------|---------|-----------------|------|
| 1 | Ischemic Heart Disease | 120.5 | Noncommunicable |
| 2 | Stroke | 94.9 | Noncommunicable |
| 3 | Neonatal Conditions | 65.5 | Communicable/Maternal |
| 4 | COPD | 57.5 | Noncommunicable |
| 5 | Diabetes Mellitus | 46.1 | Noncommunicable |
| 6 | Road Injuries | 43.2 | Injuries |
| 7 | Lung Cancer | 34.2 | Noncommunicable |
| 8 | Back/Neck Pain | 32.7 | Noncommunicable |
| 9 | Tuberculosis | 32.4 | Communicable |
| 10 | Lower Respiratory Infections | 31.5 | Communicable |

### Disease Category Distribution
- **Noncommunicable diseases**: 76 conditions (58%)
- **Communicable/maternal/nutritional**: 45 conditions (34%)
- **Injuries**: 10 conditions (8%)

## Hierarchical Disease Structure

### ICD-11 Based Organization
Our approach organizes diseases according to WHO ICD-11 chapters:

```
Chapter (Depth 0)           Condition (Depth 1)
├── cardiovascular/         ├── ischemic-heart-disease
│                          ├── stroke  
│                          └── hypertensive-heart-disease
├── respiratory/           ├── copd
│                          └── asthma
└── infectious-communicable/ ├── tuberculosis
                           ├── lower-respiratory-infections
                           └── diarrheal-diseases
```

### Standardized Format
Each disease item contains:
- **Hierarchical Path**: `cardiovascular/ischemic-heart-disease`
- **DALY Metrics**: Total burden, per-100k rates, global ranking
- **WHO Codes**: Official ICD-11 classification codes
- **Metadata**: Disease type, burden category, examples

## Implementation Files

### Core Analysis Scripts
- `analyze_daly_data.py`: Raw data processing and statistical analysis
- `generate_diseases_json.py`: Creates standardized disease dimension
- `skill_mix_dimensions_model.py`: Pydantic models for validation

### Output Files
- `data/analysis/global_daly_statistics.json`: Complete analysis results
- `data/analysis/daly_summary.json`: Summary statistics
- `clinical-skill-mix/diseases.json`: Standardized disease dimension

## Key Advantages

### 1. Evidence-Based Selection
- **Objective Prioritization**: Diseases ranked by actual global burden
- **WHO Authority**: Uses official international health statistics
- **Transparent Methodology**: Reproducible analysis pipeline

### 2. Clinical Relevance
- **Real-World Impact**: Reflects actual disease burden patterns
- **Resource Allocation**: Prioritizes high-impact conditions
- **Training Alignment**: Focuses education on prevalent diseases

### 3. Systematic Structure
- **Hierarchical Organization**: Enables flexible depth selection
- **Standardized Format**: Consistent across all skill-mix dimensions  
- **Multiplexable**: Ready for skill-mix combination analysis

## Limitations and Considerations

### Data Coverage Limitations
- **Geographic**: Limited to top 25 economies (not fully global)
- **Temporal**: 2019 baseline (pre-COVID-19 disruption)
- **Resolution**: Aggregated data, not individual-level

### Methodological Considerations
- **Aggregation Method**: Sums pre-calculated WHO values
- **Uncertainty**: Point estimates only (no confidence intervals)
- **Weighting**: Equal country weighting regardless of population size

### Interpretive Caveats
- **Regional Variation**: Global rankings may not reflect local priorities
- **Emerging Diseases**: Recent epidemics not captured in 2019 data
- **Healthcare Context**: Burden patterns vary by health system capacity

## Future Enhancements

### Potential Improvements
1. **Expanded Coverage**: Include all WHO member countries
2. **Temporal Updates**: Incorporate post-2019 data including COVID-19 impact
3. **Uncertainty Quantification**: Add confidence intervals and sensitivity analysis
4. **Regional Stratification**: Provide burden estimates by WHO regions
5. **Dynamic Updates**: Automated pipeline for new WHO data releases

### Integration Opportunities
- **Clinical Guidelines**: Link to evidence-based treatment protocols
- **Training Curricula**: Align medical education with burden patterns
- **Resource Planning**: Support healthcare system capacity planning
- **Research Priorities**: Guide funding allocation and research focus

## Citation and Attribution

### Data Source
World Health Organization. Global Health Estimates 2021: Disease burden by Cause, Age, Sex, by Country and by Region, 2000-2021. Geneva: World Health Organization; 2021.

### Methodology Reference
Murray, C.J.L., et al. Disability-adjusted life years (DALYs) for 291 diseases and injuries in 21 regions, 1990–2010: a systematic analysis for the Global Burden of Disease Study 2010. *The Lancet*. 2012;380(9859):2197-2223.

### Repository
This analysis is part of the Clinical World Model project for developing evidence-based clinical skill-mix frameworks.

---

*Last Updated: January 30, 2025*  
*Analysis Version: 1.0*  
*Data Version: WHO GHE 2021*