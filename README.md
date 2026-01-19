# Clinical World Model

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue)](https://sdamirsa.github.io/Clinical-World-Model)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An evidence-based framework for modeling clinical environments through the Clinical Skill-Mix, which operationalizes contextual dimensions via five constituent elements that decompose the clinical environment for AI deployment and evaluation.

## 🌟 Features

- **Clinical Skill-Mix Cube**: Multidimensional space with 41,061,216 unique clinical scenario cells (98 diseases × 7 stages × 12 locations × 58 tasks × 86 personas)
- **Interactive Web Interface**: Explore components through our [GitHub Pages website](https://sdamirsa.github.io/Clinical-World-Model)
- **Evidence-Based Disease Prioritization**: Global Burden of Diseases taxonomy with WHO DALY 2021 data and ICD-11 classification
- **Standardized Data Models**: Pydantic-based JSON format for all components
- **Hierarchical Structure**: Multi-level organization supporting different analysis depths
- **5-Component Framework**: Disease, Stage, Location, Task, and Persona for comprehensive clinical coverage

## 🏥 Clinical Skill-Mix Components

### 1. **Disease** (98 conditions, 14 ICD-11 chapters)
Disease list utilizing Global Burden of Diseases taxonomy for population health impact prioritization:
- Evidence-based ranking with high/medium/low DALY burden
- ICD-11 coding for deployment tracking and performance monitoring
- Explicit disease-specific capabilities rather than assumed generalization
- Hierarchical organization from chapters to specific conditions
- Cardiovascular, respiratory, neurological, infectious diseases, and more

### 2. **Stage** (7 milestones, 6 actionable stages)
Disease stage representing the temporal dimension of illness:
- **Seven Milestones**: Health → Pathologic process → Illness manifestation → Diagnosis → Treatment → Follow-up → (Cure/Disability/Death)
- **Six Actionable Stages**:
  - At-risk identification
  - Pre-symptomatic detection
  - Diagnostic workup
  - Treatment planning
  - Post-treatment care
  - Longitudinal follow-up (including coping support)
- Patients may occupy multiple positions simultaneously
- Integrated with location of care across patient journey

### 3. **Location** (12 care settings)
Location of care intrinsically linked to disease stage:
- Community screening, home-based care, outpatient clinics
- Emergency departments, inpatient wards, intensive care units
- Operating rooms, rehabilitation facilities, telemedicine
- Alternative framework: SEIPS (Systems Engineering Initiative for Patient Safety)
- Integrated with disease stage for comprehensive patient journey mapping

### 4. **Task** (58 competencies, 8 domains)
Cognitive tasks that intelligent systems aim to augment or automate:
- **Framework**: Physician Competency Reference Set (Englander et al.)
- **Eight Domains**: Patient Care, Medical Knowledge, Practice-Based Learning and Improvement, Interpersonal and Communication Skills, Professionalism, Systems-Based Practice, Interprofessional Collaboration, Personal and Professional Development
- **Alternative**: MedHELM framework (121 medical tasks, 5 categories)
- Anchored in actual cognitive work physicians perform
- Principled decisions about automation vs. augmentation

### 5. **Persona** (86 personas, 5 WHO groupings)
Caregiver persona capturing role and level of expertise:
- **Framework**: WHO International Classification of Health Workers (based on ISCO-08)
- **Total Personas**: 86 (37 Clinicians, 49 Healthcare Workers)
- **Five Broad Groupings**:
  1. Health professionals
  2. Health associate professionals
  3. Personal care workers in health services
  4. Health management and support personnel
  5. Other health service providers
- **Skill-Mix Cells**: 41,061,216 total clinical scenarios (17.7M Clinicians / 23.4M HCW)
- Identifies whose work the intelligent system aims to support

## 🚀 Quick Start

### Interactive Website
Visit our [live demo](https://sdamirsa.github.io/Clinical-World-Model) to explore the Clinical Skill-Mix Cube interactively.

### Local Development
```bash
# Clone the repository
git clone https://github.com/sdamirsa/Clinical-World-Model.git
git clone https://github.com/sdamirsa/Clinical-World-Model.git
cd Clinical-World-Model

# Install Python dependencies for data processing
pip install pandas pydantic

# Generate component data
python code/analyze_daly_data.py
python code/generate_diseases_json.py
python code/generate_personas_from_who.py

# Sync data to website folder (after any changes to clinical-skill-mix/)
cp -r clinical-skill-mix/* docs/clinical-skill-mix/

# Serve the website locally
cd docs && python -m http.server 8000
# Visit http://localhost:8000
```

## 📊 Data Sources

- **Global Burden of Diseases**: Disease taxonomy for population health impact
- **WHO DALY 2021**: Global disease burden data (2019 pre-COVID)
- **ICD-11**: Disease classification for deployment tracking
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
│   ├── task.json                  # Cognitive tasks (to augment/automate)
│   ├── persona.json               # Caregiver personas (role & expertise)
│   ├── disease.json               # Disease list (GBD/ICD-11)
│   ├── stage.json                 # Disease stages (temporal dimension)
│   ├── location.json              # Location of care (care settings)
│   └── skill_mix_dimensions_model.py # Pydantic data models
├── code/                          # 🔧 Data processing scripts
├── data/                          # 📈 Raw WHO DALY data
└── README_diseasesDALY.md         # DALY analysis documentation
```

## 💡 Use Cases

### Healthcare AI Evaluation
Create comprehensive test scenarios using the Clinical Skill-Mix Cube:
```python
# Example: Emergency medicine scenario cell in the Cube
scenario = {
    "disease": "cardiovascular/acute-myocardial-infarction",
    "stage": "diagnostic-workup",
    "location": "emergency-department",
    "task": "clinical-decision-support",
    "persona": "emergency-physician"
}
# Total cells in the Cube: 98 × 7 × 12 × 58 × 86 = 41,061,216 clinical scenarios
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

The Clinical Skill-Mix is grounded in established clinical standards:

- **Disease Component**: Global Burden of Diseases taxonomy and WHO DALY data for population health impact
- **Stage Component**: Seven milestones and six actionable stages across the patient journey
- **Location Component**: Real-world care delivery settings with SEIPS framework integration
- **Task Component**: Physician Competency Reference Set (58 competencies, 8 domains) and MedHELM framework
- **Persona Component**: WHO International Classification of Health Workers (five broad groupings)

## 🤝 Contributing

We welcome contributions to expand and refine the Clinical Skill-Mix:

1. **Data Enhancement**: Add new components or refine existing ones
2. **Analysis Tools**: Develop Clinical Skill-Mix Cube analysis capabilities
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
  note={Clinical Skill-Mix Cube: Five constituent elements for AI deployment and evaluation}
}
```

---

**Built with evidence-based medicine principles for the future of healthcare AI evaluation.** 
