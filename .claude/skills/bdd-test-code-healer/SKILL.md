---
name: bdd-test-code-healer
description: Automatically diagnoses and fixes failing BDD tests. Use when tests fail and you need to identify root causes and apply fixes. Analyzes test failures (locators, timing, data issues), proposes fixes with approval gate, applies changes, and verifies fixes work. Supports multiple feature files and retries up to 3 times.
---

# BDD Test Code Healer

Automatically diagnose and fix failing BDD tests with intelligent analysis and iterative repair.

## Quick Reference

📖 **[Examples](references/examples.md)** - 3 healing scenarios with before/after
📖 **[Best Practices](references/best-practices.md)** - 5 practices for effective healing
📖 **[Testing](references/testing.md)** - How to verify skill works
📖 **[Error Handling](references/error-handling.md)** - 5 error scenarios and solutions
📖 **[Failure Patterns Guide](references/failure-patterns.md)** - 15 failure patterns with fixes
📖 **[Implementation Guide](references/implementation-guide.md)** - All 3 phases detailed steps

---

## What It Does

Takes failing BDD tests → Runs tests → Analyzes failures (stack traces, screenshots, logs) → Identifies root causes (locators, timing, data) → Proposes fixes → Applies after approval → Verifies → Retries up to 3 times

**Use when**: Previously passing tests now fail, need quick diagnosis, UI changes broke locators, timing/flaky tests, data updates needed, want automated debugging
**Don't use**: New tests never worked (use `/bdd-test-code-generator`), writing new scenarios, legitimate application bugs

**Features**: Intelligent failure analysis (15+ patterns), Approval gate, Iterative repair (3 attempts max), Multiple feature support, Headed mode, Clear progress reporting

---

## Configuration

Tests run in **headed mode** (`--headed`) with **stop-on-first-failure** (`-x`) for better visibility, faster healing, and avoiding cascade failures. All analysis reports use emojis, tables, and clear sections.

---

## Quick Start

```bash
# Fix single feature file
/bdd-test-code-healer task_crud_operations.feature

# Fix multiple feature files
/bdd-test-code-healer task_crud_operations.feature,pipeline_workflow.feature

# Or with full path
/bdd-test-code-healer tests/features/task_crud_operations.feature
```

---

## Healing Workflow

**Phase 1** (Test Execution & Analysis): Run tests (`pytest --headed -x`) → Stop on first failure → Capture results → Parse failures → Analyze patterns → Identify root cause → Propose fix → **🛑 STOP** - Wait for approval

**Phase 2** (Fix Application & Verification): Apply fix → Re-run tests → Check results → Report outcome

**Phase 3** (Iterative Repair): If still failing → Analyze new failure → Propose new fix → Wait for approval → Repeat (max 3 attempts)

---

## Input Formats

| Format | Example | Result |
|--------|---------|--------|
| **Single file** | `/bdd-test-code-healer task_crud.feature` | Runs and heals one feature |
| **Multiple files** | `/bdd-test-code-healer file1.feature,file2.feature` | Runs all, heals each that fails |
| **Full path** | `/bdd-test-code-healer tests/features/task_crud.feature` | Accepts absolute or relative paths |

---

## Prerequisites

pytest + pytest-bdd installed, Tests have run before, Environment configured (`.env`), OpenShift cluster accessible, Test data exists (`framework/resources/test_data/`), POM framework (`framework/ui_components/`)

---

## Common Failure Patterns Detected

Recognizes 15+ patterns: Locator not found, Element not visible/clickable, Timeout, StaleElementReference, Assertion failed, FileNotFoundError, YAML parsing, Authentication failure, Project creation, Navigation failure, Step definition not found, Import/Attribute/Type errors. See [Failure Patterns Guide](references/failure-patterns.md)

---

## Approval Gate Details

**The skill NEVER applies fixes without explicit user approval.**

Each report shows: Test failure details, Root cause analysis, Proposed fix (before/after), Affected files, Rationale

**Your options**: "yes" (apply), "no" (skip), "show me the error" (full trace), "try X instead" (suggest alternative)

---

## Iterative Repair Strategy

**Attempt 1**: Most common fix for pattern
**Attempt 2**: Same error → Adjust (longer timeout, different locator); Different error → Address new cause
**Attempt 3**: Fallback approach
**After 3**: Report tries, recommend manual investigation

---

## Limitations

UI-only test fixes, Cannot fix app bugs, Requires runnable tests, No interactive debugging, Pattern-based (may miss novel scenarios), Max 3 attempts

---

## Related Skills

- **`/bdd-test-code-generator`** - Generate new tests from plain English
- **`/multi-page-pom`** - Regenerate page objects if UI changed significantly

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: 2026-05-02
