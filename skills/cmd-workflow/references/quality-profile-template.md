# QUALITY_PROFILE

## Metadata
- Task ID:
- Risk Level: Low / Medium / High
- Owner:
- Date:

## 1) Risk Classification Rationale
- Why this risk level:
- Primary failure modes:

## 2) Gate Matrix
| Gate | Low | Medium | High | Evidence Type |
| --- | --- | --- | --- | --- |
| Lint / Format | Required | Required | Required | Command output |
| Type Check | Required | Required | Required | Command output |
| Test-First Evidence (Red) | Optional | Required | Required | Failing test run log |
| Unit Tests (touched areas) | Optional | Required | Required | Test report |
| Integration / API Tests | Optional | Recommended | Required | Test report |
| Refactor Safety Pass (Green) | Optional | Required | Required | Passing test report |
| Security Checklist | Optional | Recommended | Required | Checklist |
| Rollback Plan | Optional | Required | Required | Written plan |

## 3) Quality Rules
| Rule ID | Dimension | Requirement | Verification Method | Pass/Fail |
| --- | --- | --- | --- | --- |
| QR-01 | Correctness | Acceptance criteria are all testable | Contract mapping |  |
| QR-02 | Architecture | Boundaries and layering rules are respected | Code review + static checks |  |
| QR-03 | Security | No secrets, no sensitive detail leakage | Checklist + grep |  |
| QR-04 | Maintainability | Clear naming and minimal localized changes | Diff review |  |
| QR-05 | Observability | Errors are diagnosable without exposing internals | Log/error surface review |  |
| QR-06 | TDD Compliance | Medium/high-risk changes follow required test-first policy | Red/green evidence + review |  |

## 4) Verification Commands
| Step | Command | Expected Result |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

## 5) TDD Evidence Log
| Behavior / AC | Test(s) Added First | Initial Result (Red) | Final Result (Green) | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

## 6) Exception Triggers
Escalate to developer if any trigger is true:
- Security/auth/privacy boundary is ambiguous.
- Behavior change conflicts with expected business rule.
- Data-loss or irreversible migration risk appears.
- Confidence drops below acceptable threshold.
- Required test-first flow is blocked with no safe fallback.

## 7) Rollback Strategy
- Rollback trigger:
- Rollback method:
- Data recovery notes:
- Owner:
