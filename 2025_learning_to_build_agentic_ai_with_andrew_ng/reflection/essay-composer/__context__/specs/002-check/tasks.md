# Implementation Tasks: Test Fix Implementation

**Feature**: Check Feature - Fix 21 Failing Tests  
**Created**: 2024-12-19  
**Status**: Ready for Implementation  

## Task Overview

**Total Tasks**: 15  
**Estimated Time**: 7-10 hours  
**Priority**: CRITICAL → HIGH → MEDIUM → LOW  

## Phase 1: Setup and Analysis (30 minutes)

### Task 1.1: Environment Setup
- **ID**: SETUP-001
- **Description**: Set up development environment and verify current test status
- **Files**: `pyproject.toml`, `uv.lock`
- **Actions**:
  - Install dependencies with `uv sync`
  - Run current test suite to capture baseline
  - Document current failure patterns
- **Dependencies**: None
- **Validation**: All dependencies installed, test suite runs

### Task 1.2: Test Failure Analysis
- **ID**: SETUP-002  
- **Description**: Analyze and categorize all 21 test failures
- **Files**: `__context__/bugfix.md`
- **Actions**:
  - Parse test failure output
  - Categorize by type (CLI, Integration, ADK, Prompts)
  - Prioritize by impact (CRITICAL, HIGH, MEDIUM, LOW)
- **Dependencies**: SETUP-001
- **Validation**: Complete failure categorization documented

## Phase 2: Critical Fixes - ADK Agents (2-3 hours)

### Task 2.1: Fix SequentialAgent Validation
- **ID**: ADK-001
- **Description**: Fix pydantic validation errors in SequentialAgent initialization
- **Files**: `src/agents/orchestrator.py`
- **Actions**:
  - Review Google ADK documentation for SequentialAgent usage
  - Fix parameter types and validation
  - Add proper error handling for missing dependencies
- **Dependencies**: SETUP-002
- **Validation**: `tests/test_adk_agents.py::TestEssayComposerOrchestrator::test_init` passes

### Task 2.2: Fix Agent Attribute Access
- **ID**: ADK-002
- **Description**: Resolve attribute access errors in orchestrator
- **Files**: `src/agents/orchestrator.py`
- **Actions**:
  - Fix attribute access patterns
  - Update agent initialization
  - Improve error handling
- **Dependencies**: ADK-001
- **Validation**: `tests/test_adk_agents.py::TestEssayComposerOrchestrator::test_get_workflow_info` passes

### Task 2.3: Verify ADK Agent Fixes
- **ID**: ADK-003
- **Description**: Run ADK agent tests to verify all fixes
- **Files**: `tests/test_adk_agents.py`
- **Actions**:
  - Run `uv run python -m pytest tests/test_adk_agents.py -v`
  - Verify all ADK-related tests pass
  - Document any remaining issues
- **Dependencies**: ADK-002
- **Validation**: All ADK agent tests pass

## Phase 3: High Priority Fixes - CLI & Integration (3-4 hours)

### Task 3.1: Add Missing CLI Options
- **ID**: CLI-001
- **Description**: Add missing --legacy CLI option to essay_composer.py
- **Files**: `src/essay_composer.py`
- **Actions**:
  - Add --legacy option to Click command
  - Implement legacy mode functionality
  - Update help text and documentation
- **Dependencies**: ADK-003
- **Validation**: CLI help shows --legacy option

### Task 3.2: Fix CLI Mock Setup
- **ID**: CLI-002
- **Description**: Fix mock setup for CLI E2E tests
- **Files**: `tests/e2e/test_cli_e2e.py`
- **Actions**:
  - Fix mock setup for external dependencies
  - Update output assertions to match actual behavior
  - Improve error handling in CLI interface
- **Dependencies**: CLI-001
- **Validation**: CLI E2E tests pass

### Task 3.3: Fix Integration Test Mocking
- **ID**: INT-001
- **Description**: Fix mock object subscriptability in integration tests
- **Files**: `tests/integration/test_agent_integration.py`
- **Actions**:
  - Use MagicMock instead of Mock for subscriptable objects
  - Fix variable scope issues in test setup
  - Improve mock configuration for complex objects
- **Dependencies**: CLI-002
- **Validation**: Integration tests pass

### Task 3.4: Verify CLI and Integration Fixes
- **ID**: VERIFY-001
- **Description**: Run CLI and integration tests to verify all fixes
- **Files**: `tests/e2e/test_cli_e2e.py`, `tests/integration/test_agent_integration.py`
- **Actions**:
  - Run CLI E2E tests
  - Run integration tests
  - Document any remaining issues
- **Dependencies**: INT-001
- **Validation**: All CLI and integration tests pass

## Phase 4: Medium Priority Fixes - Prompts (1-2 hours)

### Task 4.1: Update Generator Prompts
- **ID**: PROMPT-001
- **Description**: Update generator prompt templates to match test expectations
- **Files**: `src/prompts.py`
- **Actions**:
  - Add missing keywords like "well-structured essay"
  - Update prompt content structure
  - Validate prompt formatting
- **Dependencies**: VERIFY-001
- **Validation**: Generator prompt tests pass

### Task 4.2: Update Reflector Prompts
- **ID**: PROMPT-002
- **Description**: Update reflector prompt templates
- **Files**: `src/prompts.py`
- **Actions**:
  - Add "Structure and Organization" keywords
  - Update prompt content structure
  - Validate prompt formatting
- **Dependencies**: PROMPT-001
- **Validation**: Reflector prompt tests pass

### Task 4.3: Update Revision Prompts
- **ID**: PROMPT-003
- **Description**: Update revision prompt templates
- **Files**: `src/prompts.py`
- **Actions**:
  - Add "incorporating the feedback" keywords
  - Update prompt content structure
  - Validate prompt formatting
- **Dependencies**: PROMPT-002
- **Validation**: Revision prompt tests pass

### Task 4.4: Verify Prompt Fixes
- **ID**: PROMPT-004
- **Description**: Run all prompt tests to verify fixes
- **Files**: `tests/test_prompts.py`, `tests/unit/test_prompts_unit.py`
- **Actions**:
  - Run prompt tests
  - Run unit prompt tests
  - Document any remaining issues
- **Dependencies**: PROMPT-003
- **Validation**: All prompt tests pass

## Phase 5: Performance Optimization (1 hour)

### Task 5.1: Optimize Test Execution
- **ID**: PERF-001
- **Description**: Optimize test execution time and performance
- **Files**: `pyproject.toml`, test files
- **Actions**:
  - Add pytest-xdist for parallel execution
  - Optimize mock setup to reduce overhead
  - Cache expensive operations in tests
- **Dependencies**: PROMPT-004
- **Validation**: Test execution time < 60 seconds

### Task 5.2: Performance Validation
- **ID**: PERF-002
- **Description**: Measure and validate performance improvements
- **Files**: Test configuration
- **Actions**:
  - Measure current execution time
  - Compare with target (< 60 seconds)
  - Document performance improvements
- **Dependencies**: PERF-001
- **Validation**: Performance targets met

## Phase 6: Final Validation and Documentation (30 minutes)

### Task 6.1: Complete Test Suite Validation
- **ID**: FINAL-001
- **Description**: Run complete test suite to verify all fixes
- **Files**: All test files
- **Actions**:
  - Run full test suite
  - Verify 100% test pass rate (81/81)
  - Document final results
- **Dependencies**: PERF-002
- **Validation**: All 81 tests pass

### Task 6.2: Documentation Update
- **ID**: FINAL-002
- **Description**: Update test documentation and create summary
- **Files**: `README.md`, test documentation
- **Actions**:
  - Update test documentation
  - Create implementation summary
  - Document lessons learned
- **Dependencies**: FINAL-001
- **Validation**: Documentation updated

## Execution Rules

### Sequential Tasks
- Setup tasks must complete before development tasks
- ADK fixes must complete before CLI fixes
- CLI fixes must complete before prompt fixes
- All fixes must complete before performance optimization

### Parallel Tasks [P]
- None in this implementation (all tasks are sequential due to dependencies)

### File Coordination
- Tasks affecting `src/agents/orchestrator.py` must run sequentially
- Tasks affecting `src/essay_composer.py` must run sequentially  
- Tasks affecting `src/prompts.py` must run sequentially
- Test files can be updated in parallel with their corresponding source files

### Validation Checkpoints
- After each phase, run relevant tests to verify fixes
- Document any failures or issues encountered
- Ensure no regressions are introduced

## Success Criteria

- **Test Pass Rate**: 100% (81/81 tests passing)
- **Execution Time**: < 60 seconds for full test suite
- **Code Coverage**: Maintain or improve current coverage
- **Regression Prevention**: No new test failures introduced

## Risk Mitigation

- **Incremental Fixes**: Fix one category at a time
- **Validation**: Run tests after each fix
- **Rollback**: Git commit after each successful fix
- **Documentation**: Update test documentation as needed
