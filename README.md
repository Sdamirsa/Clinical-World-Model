# Clinical World Model

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue)](https://sdamirsa.github.io/Clinical-World-Model)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An evidence-based framework for modeling clinical environments through Clinical Competency Space (5C) and AI Cognitive Engagement (3A), creating an 8-dimensional Clinical Intelligence space for comprehensive healthcare AI evaluation.

## 🌟 Features

- **Clinical Competency Cube (5C)**: Multidimensional space with 803,626,656 unique clinical scenario cells (1,918 conditions × 7 care phases × 12 care settings × 58 care tasks × 86 care provider roles)
- **AI Cognitive Engagement Cube (3A)**: 3-dimension framework capturing how AI engages with clinical workflows (Agent Facing × Anchoring Layer × Assigned Authority)
- **Clinical Intelligence Space**: 5C × 3A = 8-dimensional space (803.6M clinical scenarios × 84 AI engagement patterns = 67.5B unique cells)
- **Interactive Web Interface**: Explore both cubes through our [GitHub Pages website](https://sdamirsa.github.io/Clinical-World-Model)
- **Standardized Condition Classification**: ICD-10-CM major category codes (3-character) for comprehensive disease coverage
- **Standardized Data Models**: Pydantic-based JSON format for all components
- **Hierarchical Structure**: Multi-level organization supporting different analysis depths

## 🏥 Clinical Competency Dimensions

### 1. **Condition** (1,918 codes, 26 ICD-10-CM chapters)
Medical conditions using ICD-10-CM 3-character codes (complete coverage):
- Comprehensive coverage across all disease chapters (A-Z)
- Standardized clinical terminology (1,918 3-character codes across 26 chapters)
- ICD-10-CM clinical modification used worldwide for medical coding
- Explicit condition-specific capabilities rather than assumed generalization
- Hierarchical organization from chapters to major category codes
- Covers all disease categories: infectious, neoplasms, circulatory, respiratory, endocrine, mental health, and more

### 2. **Care Phase** (7 phases)
Temporal dimension of illness representing the patient journey:
- **Seven Phases**:
  1. At-Risk Identification
  2. Pre-Symptomatic Detection
  3. Diagnostic Workup
  4. Treatment Planning
  5. Post-Treatment Care
  6. Longitudinal Follow-Up
  7. Coping Support
- Patients may occupy multiple positions simultaneously
- Integrated with care settings across patient journey
- Maps to clinical milestones: Health → Pathologic Process → Illness → Diagnosis → Treatment → Follow-up → Cure/Disability/Death

### 3. **Care Setting** (12 settings)
Location of care delivery intrinsically linked to care phase:
- Community screening, home-based care, outpatient clinics
- Emergency departments, inpatient wards, intensive care units
- Operating rooms, rehabilitation facilities, telemedicine
- Alternative framework: SEIPS (Systems Engineering Initiative for Patient Safety)
- Integrated with care phase for comprehensive patient journey mapping

### 4. **Care Task** (58 competencies, 8 domains)
Cognitive tasks that intelligent systems aim to augment or automate:
- **Framework**: Physician Competency Reference Set (Englander et al.)
- **Eight Domains**: Patient Care, Medical Knowledge, Practice-Based Learning and Improvement, Interpersonal and Communication Skills, Professionalism, Systems-Based Practice, Interprofessional Collaboration, Personal and Professional Development
- **Alternative**: MedHELM framework (121 medical tasks, 5 categories)
- Anchored in actual cognitive work physicians perform
- Principled decisions about automation vs. augmentation

### 5. **Care Provider Role** (86 roles, WHO classification)
Healthcare professional role capturing expertise level:
- **Framework**: WHO International Classification of Health Workers (based on ISCO-08)
- **Total Roles**: 86 (51 major categories + 35 specialized subcategories)
- **Five Broad Groupings**:
  1. Health professionals (physicians, nurses, pharmacists, dentists, etc.)
  2. Health associate professionals (nursing associates, medical assistants, etc.)
  3. Personal care workers in health services
  4. Health management and support personnel
  5. Other health service providers
- Identifies whose work the intelligent system aims to support
- Includes specialist medical practitioners across 35 medical specialties

## 🧠 AI Cognitive Engagement Dimensions (3A)

### 1. **Agent Facing** (4 options)
Defines whose cognition AI engages:
- **Provider-Facing**: Healthcare provider perspective (CDM model)
- **Patient-Facing**: Patient perspective (PDM model)
- **Encounter-Facing**: System-level interaction perspective (CDM + PDM)
- **Ecosystem-Facing**: Population and organizational systems perspective (EDM)

### 2. **Anchoring Layer** (7 layers)
Specifies the point in cognitive architecture where AI intervenes:
- **Input**: Data entry and acquisition
- **Data Processor**: Information processing and transformation
- **Hypothesis**: Differential diagnosis and hypothesis generation
- **System I**: Intuitive, pattern-recognition reasoning
- **System II**: Analytical, deliberative reasoning
- **Reflection**: Metacognitive evaluation and learning
- **Action**: Decision execution and implementation

### 3. **Assigned Authority** (3 levels)
Specifies the degree of AI cognitive takeover:
- **Monitoring**: AI observes and flags issues for human review (Observer role)
- **Augmentation**: AI provides supportive recommendations while human retains decision authority (Supportive contributor)
- **Automation**: AI executes decisions autonomously with human oversight for exceptions (Primary processor)

## 🚀 Quick Start

### Interactive Website
Visit our [live demo](https://sdamirsa.github.io/Clinical-World-Model) to explore the Clinical Competency (5C) and AI Cognitive Engagement (3A) cubes interactively.

### Local Development
```bash
# Clone the repository
git clone https://github.com/sdamirsa/Clinical-World-Model.git
cd Clinical-World-Model

# Install Python dependencies for data processing
pip install pandas pydantic

# Generate 5C dimension data
python code/generate_conditions_json.py
python code/generate_care_phases_json.py
python code/generate_care_settings_json.py
python code/generate_care_task_json.py
python code/generate_care_provider_role_json.py

# Generate 3A dimension data
python code/generate_agent_facing_json.py
python code/generate_anchoring_layer_json.py
python code/generate_assigned_authority_json.py

# Sync data to website folder (after any changes to clinical-skill-mix/)
cp -r clinical-skill-mix/* docs/clinical-skill-mix/

# Serve the website locally
cd docs && python -m http.server 8000
# Visit http://localhost:8000
```

## 📊 Data Sources

- **ICD-10-CM**: International Classification of Diseases, 10th Revision, Clinical Modification
  - All 3-character codes (e.g., I25, C50, J44) - complete coverage
  - Source: Centers for Medicare & Medicaid Services (CMS), WHO ICD-10 base
  - 1,918 codes across 26 disease chapters
- **ICD-11**: Condition classification for deployment tracking
- **WHO International Classification of Health Workers**: Five broad professional groupings
- **ISCO-08**: International Standard Classification of Occupations
- **Physician Competency Reference Set**: 58 competencies across 8 domains (Englander et al.)
- **MedHELM Framework**: 121 medical tasks in 5 categories
- **SEIPS Framework**: Patient journey modeling across care settings

## 🏗️ Architecture

```
Clinical-World-Model/
├── docs/                          # 🌐 GitHub Pages website
│   ├── index.html                 # Main website entry point
│   ├── _config.yml                # GitHub Pages configuration
│   ├── clinical-skill-mix/        # 📊 Component data (copy for website)
│   └── assets/                    # Website assets
│       ├── css/styles.css         # Modern responsive design
│       └── js/                    # Interactive functionality
├── clinical-skill-mix/            # 📊 Source component data
│   ├── competency_domains.json    # Competency domains (to augment/automate)
│   ├── provider_roles.json        # Provider roles (role & expertise)
│   ├── conditions.json            # Conditions (GBD/ICD-11)
│   ├── care_phases.json           # Care phases (temporal dimension)
│   ├── care_settings.json         # Care settings (location of care)
│   ├── agent.json                 # Cognitive Engagement: Agent
│   ├── reasoning_layer.json       # Cognitive Engagement: Reasoning Layer
│   ├── integration_mode.json      # Cognitive Engagement: Integration Mode
│   ├── temporality.json           # Cognitive Engagement: Temporality
│   └── skill_mix_dimensions_model.py # Pydantic data models
├── code/                          # 🔧 Data processing scripts
├── data/                          # 📈 Raw WHO DALY data
└── README_diseasesDALY.md         # DALY analysis documentation
```

## 💡 Use Cases

### Healthcare AI Evaluation
Create comprehensive test scenarios using the Clinical Intelligence space:
```python
# Example: Emergency medicine scenario in Clinical Competency Cube
clinical_competency = {
    "condition": "cardiovascular/acute-myocardial-infarction",
    "care_phase": "diagnostic-workup",
    "care_setting": "emergency-department",
    "competency_domain": "clinical-decision-support",
    "provider_role": "emergency-physician"
}
# Clinical Competency Cube: 98 × 7 × 12 × 58 × 86 = 41,061,216 scenarios

# Example: AI engagement specification in Cognitive Engagement Cube
cognitive_engagement = {
    "agent": "clinician",
    "reasoning_layer": "hypothesis",
    "integration_mode": "augment",
    "temporality": "concurrent"
}
# Cognitive Engagement Cube: 4 × 7 × 3 = 84 engagement scenarios

# Clinical Intelligence = Clinical Competency × Cognitive Engagement
# Total distinct capability claims requiring evaluation
```

### Clinical Education
- **Competency Mapping**: Align training with evidence-based skill requirements
- **Scenario Generation**: Create realistic clinical cases across settings
- **Assessment Design**: Develop comprehensive evaluation frameworks

### Health System Analysis
- **Resource Planning**: Model care delivery across different resource settings
- **Workflow Optimization**: Analyze task distributions across provider roles
- **Quality Improvement**: Evidence-based approach to care standardization

## 📈 Evidence Base

The Clinical World Model is grounded in established clinical standards:

**Clinical Competency Dimensions**:
- **Condition**: Global Burden of Diseases taxonomy and WHO DALY data for population health impact
- **Care Phase**: Seven milestones and six actionable phases across the patient journey
- **Care Setting**: Real-world care delivery settings with SEIPS framework integration
- **Competency Domain**: Physician Competency Reference Set (58 competencies, 8 domains) and MedHELM framework
- **Provider Role**: WHO International Classification of Health Workers (five broad groupings)

**Cognitive Engagement Aspects**:
- **Agent**: Clinician, Patient, Encounter, and Ecosystem perspectives
- **Reasoning Layer**: Seven cognitive architecture layers from dual-process theory
- **Integration Mode**: Three modes of AI-workflow integration
- **Temporality**: Three timeframes for AI intervention

## 🤝 Contributing

We welcome contributions to expand and refine the Clinical World Model:

1. **Data Enhancement**: Add new components or refine existing ones
2. **Analysis Tools**: Develop Clinical Intelligence space analysis capabilities
3. **Validation Studies**: Test framework applicability in real clinical settings
4. **Integration**: Connect with existing healthcare AI evaluation tools

## 📖 Documentation

- [DALY Analysis Methodology](README_diseasesDALY.md) - Disease prioritization approach
- [Data Model Specification](clinical-skill-mix/skill_mix_dimensions_model.py) - Pydantic schemas
- [Interactive Website](https://sdamirsa.github.io/Clinical-World-Model) - Live exploration tool
- [Interactive Website](https://sdamirsa.github.io/Clinical-World-Model) - Live exploration tool

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Citation

If you use this framework in your research, please cite:

```bibtex
@misc{clinical-world-model-2025,
  title={Beyond Pattern Recognition: The Clinical World Model Framework for Cognition-Informed Medical AI},
  author={Safavi-Naini, Seyed Amir Ahmad and Meftah, Elahe and Mohess, Josh and Kazaj, Pooya Mohammadi and Siontis, Georgios and Atf, Zahra and Vaid, Akhil and Lewis, Peter R. and Nadkarni, Girish and Windecker, Stephan and Gräni, Christoph and Soroush, Ali and Shiri, Isaac},
  year={2025},
  url={https://github.com/sdamirsa/Clinical-World-Model},
  note={Clinical Competency × Cognitive Engagement = Clinical Intelligence for AI evaluation}
}
```

---

**Built with evidence-based medicine principles for the future of healthcare AI evaluation.** 
