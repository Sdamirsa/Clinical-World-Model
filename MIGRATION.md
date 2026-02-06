# Migration Guide: v1.0 → v2.0

## Overview

Clinical World Model framework upgraded from 5-dimension single cube to **8-dimension dual-cube architecture (5C + 3A)**.

---

## Terminology Changes

### Clinical Competency Dimensions (5C)

| v1.0 Name | v2.0 Name | Data Source |
|-----------|-----------|-------------|
| Disease | **Condition** | ICD-10-CM (1,918 codes) |
| Stage | **Care Phase** | 7 patient journey phases |
| Location | **Care Setting** | 12 care delivery settings |
| Task | **Care Task** | 58 competencies (Physician Competency Reference Set) |
| Persona | **Care Provider Role** | 86 roles (WHO/ISCO-08) |

### New: AI Cognitive Engagement (3A)

| Dimension | Options | Description |
|-----------|---------|-------------|
| **Agent Facing** | 3 | Provider/Patient/Encounter perspective |
| **Anchoring Layer** | 7 | Cognitive architecture intervention point |
| **Assigned Authority** | 3 | Monitoring/Augmentation/Automation |

---

## Key Changes

### Framework Architecture
- **v1.0**: Single 5-dimension cube
- **v2.0**: Dual cubes (5C × 3A = 8 dimensions)



### Website
- **v1.0**: Single cube explorer
- **v2.0**: Two interactive cube explorers + combined Clinical Intelligence output

---

## File Changes

### Renamed Files
```bash
# JSON files
competency_domains.json → care_task.json
provider_roles.json → care_provider_role.json

# Generation scripts
generate_competency_domains_json.py → generate_care_task_json.py
generate_provider_roles_from_who.py → generate_care_provider_role_json.py
```

### Deleted Files (v1.0)
```
disease.json, stage.json, location.json, persona.json, task.json
+ corresponding generation scripts
```

### New Files (v2.0)
```
# 5C dimensions
conditions.json, care_phases.json, care_settings.json, care_task.json, care_provider_role.json

# 3A dimensions
agent_facing.json, anchoring_layer.json, assigned_authority.json

# Generation scripts for all 8 dimensions
```

---

## Migration Checklist

✅ Update dimension references in code
✅ Regenerate all 8 JSON files
✅ Update README.md with new calculations
✅ Update website with dual-cube interface
✅ Sync JSONs to `docs/clinical-skill-mix/`
✅ Update documentation (CLAUDE.md, README.md)

---

## Backward Compatibility

**Breaking Changes**: v2.0 is NOT backward compatible with v1.0 due to:
- Complete terminology overhaul
- New data structure (dual cubes)
- Different dimension names and file paths

---

## Date

**Migration Completed**: 01 February 2026
**Version**: v2.0 (8-dimension framework)
