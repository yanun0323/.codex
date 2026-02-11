---
workflow_version: v2
pr_id: {{pr_id}}
thread_key: {{thread_key}}
title: "{{title}}"
task_slug: {{task_slug}}
stage: A
status: active
created_at: {{created_at}}
updated_at: {{updated_at}}
description: "{{description}}"
---

# PR Change Card
### Business Goal: {{business_goal}}
### Out of Scope:
{{out_of_scope_lines}}

### Architecture Gate:
- Schema change: {{schema_change}}
- Auth/Permission change: {{auth_permission_change}}
- Cross-service contract change: {{cross_service_contract_change}}
- Critical invariant impact: {{critical_invariant_impact}}
- Migration required: {{migration_required}}
- Rollback path defined: {{rollback_path_defined}}

### Acceptance Tests (<=8):
{{acceptance_tests_lines}}

### Critical Invariants (<=5):
{{critical_invariants_lines}}

# Business Specification
### Problem Statement
{{problem_statement}}

### Business Context
{{business_context}}

### User Roles and Stakeholders
{{user_roles_lines}}

### Detailed Business Logic
{{detailed_business_logic_lines}}

### Functional Requirements
{{functional_requirements_lines}}

### Non-Functional Requirements
{{non_functional_requirements_lines}}

### Decision Rules and Constraints
{{decision_rules_lines}}

### Process Flow
{{process_flow_lines}}

### Edge Cases and Exceptions
{{edge_cases_lines}}

### Input Sources
Question Summary:
{{question_summary}}

Referenced Files:
{{referenced_files_lines}}

### Open Questions
{{open_questions_lines}}

# CR Checklist
| CR-ID | Scope | Goal | Path(Fast/Guarded) | Status | Evidence Link | Commit Hash |
|------|-------|------|---------------------|--------|---------------|-------------|
{{cr_rows}}
