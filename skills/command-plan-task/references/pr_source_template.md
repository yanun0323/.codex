---
workflow_version: v3
pr_id: {{pr_id}}
thread_key: {{thread_key}}
title: "{{title}}"
task_slug: {{task_slug}}
stage: Requirement Definition
status: active
created_at: {{created_at}}
updated_at: {{updated_at}}
description: "{{description}}"
---

# PR Change Card
### Business Goal: 
{{business_goal}}

### Out of Scope:
{{out_of_scope_lines}}

### Architecture Gate:
- Schema change: {{schema_change}}
- Auth/Permission change: {{auth_permission_change}}
- Cross-service contract change: {{cross_service_contract_change}}
- Critical invariant impact: {{critical_invariant_impact}}
- Migration required: {{migration_required}}
- Rollback path defined: {{rollback_path_defined}}

# Requirement Memory (Internal)
### Planning Notes (Optional)
{{planning_notes_lines}}

### Referenced Files
{{referenced_files_lines}}

### Open Questions
{{open_questions_lines}}

### Clarification Items
{{clarification_items_lines}}

# Acceptance Tests
### Acceptance Tests:
{{acceptance_tests_lines}}

### Critical Invariants:
{{critical_invariants_lines}}

# CR Checklist
| CR-ID | Scope | Scope Seq | CR Type (test/impl) | Goal | Path(Fast/Guarded) | Status | Evidence Link | Commit Hash |
|------|-------|-----------|----------------------|------|---------------------|--------|---------------|-------------|
{{cr_rows}}
