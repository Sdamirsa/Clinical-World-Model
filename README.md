# Clinical World Model

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-blue)](https://your-username.github.io/Clinical-World-Model)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, evidence-based framework for modeling clinical environments and defining clinical skill-mix to facilitate the design, evaluation, and deployment of intelligent systems for clinical use.

## 🌟 Features

- **Interactive Web Interface**: Explore dimensions through our [GitHub Pages website](https://your-username.github.io/Clinical-World-Model)
- **Evidence-Based Disease Prioritization**: WHO DALY 2021 data integration with ICD-11 classification
- **Standardized Data Models**: Pydantic-based JSON format for all dimensions
- **Hierarchical Structure**: Multi-level organization supporting different analysis depths
- **5-Dimensional Framework**: Comprehensive coverage of clinical practice aspects

## 🏥 Clinical Skill-Mix Dimensions

### 1. **Task Skills** (20 skills across 4 domains)
Clinical competencies based on CanMEDS and ACGME frameworks:
- **Data Gathering**: History-taking, physical examination, diagnostic testing
- **Clinical Reasoning**: Diagnosis, pattern recognition, evidence synthesis  
- **Intervention**: Treatment planning, procedures, medication management
- **Communication**: Patient counseling, documentation, team collaboration

### 2. **Personas** (5 roles, 20 characteristics)
Healthcare provider roles with distinct responsibilities:
- Attending physicians, residents, nurses, specialists, allied health professionals
- Based on ISCO-08 international classification standards

### 3. **Diseases** (98 conditions, 14 ICD-11 chapters)
Evidence-based disease prioritization using WHO DALY data:
- Global burden metrics with high/medium/low DALY rankings
- Cardiovascular, respiratory, neurological, infectious diseases, and more
- Hierarchical organization from chapters to specific conditions

### 4. **Timeline** (12 states, 26 transitions)
Disease progression states based on clinical pathophysiology:
- healthy → at-risk → pathologic-process → illness → diagnosis → treatment → follow-up → outcomes
- Bidirectional transitions supporting complex clinical scenarios

### 5. **Location-Resources** (24 combinations)
Healthcare delivery settings with resource availability:
- **Locations**: Pre-hospital, emergency, ICU, operating room, wards, outpatient, community, home, telemedicine
- **Resource Levels**: Limited vs. rich resource availability

## 🚀 Quick Start

### Interactive Website
Visit our [live demo](https://your-username.github.io/Clinical-World-Model) to explore dimensions interactively.

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-username/Clinical-World-Model.git
cd Clinical-World-Model

# Install Python dependencies for data processing
pip install pandas pydantic

# Generate dimension data
python code/analyze_daly_data.py
python code/generate_diseases_json.py

# Serve the website locally
cd website && python -m http.server 8000
# Visit http://localhost:8000
```

## 📊 Data Sources

- **WHO DALY 2021**: Global disease burden data
- **ICD-11**: Disease classification system
- **CanMEDS/ACGME**: Clinical competency frameworks
- **ISCO-08**: Healthcare professional classifications

## 🏗️ Architecture

```
Clinical-World-Model/
├── website/                       # GitHub Pages website
│   ├── index.html                 # Main website entry point
│   └── assets/                    # Website assets
│       ├── css/styles.css         # Modern responsive design
│       └── js/                    # Interactive functionality
├── clinical-skill-mix/            # Standardized dimension data
│   ├── task-skills.json           # Clinical competencies
│   ├── personas.json              # Healthcare provider roles
│   ├── diseases.json              # WHO DALY-prioritized conditions
│   ├── timelines.json             # Disease progression states
│   ├── location-resources.json    # Care settings & resources
│   └── skill_mix_dimensions_model.py # Pydantic data models
├── code/                          # Data processing scripts
├── data/                          # Raw WHO DALY data
├── README_diseasesDALY.md         # DALY analysis documentation
└── _config.yml                    # GitHub Pages configuration
```

## 💡 Use Cases

### Healthcare AI Evaluation
Create comprehensive test scenarios by combining dimension elements:
```python
# Example: Emergency medicine scenario
scenario = {
    "task": "emergency-diagnosis",
    "persona": "emergency-physician", 
    "disease": "cardiovascular/acute-myocardial-infarction",
    "timeline": "acute-illness",
    "location": "emergency-department/rich-resources"
}
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

Our framework is grounded in established clinical standards:

- **Disease Prioritization**: WHO DALY data covering global disease burden
- **Clinical Competencies**: International medical education frameworks
- **Care Delivery**: Real-world healthcare system organization
- **Provider Roles**: Standardized professional classifications

## 🤝 Contributing

We welcome contributions to expand and refine the Clinical World Model:

1. **Data Enhancement**: Add new dimensions or refine existing ones
2. **Analysis Tools**: Develop cross-dimensional analysis capabilities  
3. **Validation Studies**: Test framework applicability in real settings
4. **Integration**: Connect with existing healthcare AI evaluation tools

## 📖 Documentation

- [DALY Analysis Methodology](README_diseasesDALY.md) - Disease prioritization approach
- [Data Model Specification](clinical-skill-mix/skill_mix_dimensions_model.py) - Pydantic schemas
- [Interactive Website](https://your-username.github.io/Clinical-World-Model) - Live exploration tool

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Citation

If you use this framework in your research, please cite:

```bibtex
@misc{clinical-world-model-2025,
  title={Clinical World Model: Evidence-Based Framework for Healthcare AI Evaluation},
  author={[Your Name]},
  year={2025},
  url={https://github.com/your-username/Clinical-World-Model}
}
```

---

**Built with evidence-based medicine principles for the future of healthcare AI evaluation.** 
