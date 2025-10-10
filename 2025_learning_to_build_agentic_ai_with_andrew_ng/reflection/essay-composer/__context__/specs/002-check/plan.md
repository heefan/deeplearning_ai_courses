# Implementation Plan: Fix Test Failures

**Feature**: Check Feature  
**Created**: 2024-12-19  
**Status**: In Development  

## Technical Context

### Current State Analysis
- **21 test failures** across multiple test categories
- **60 tests passing** - good foundation exists
- **Test execution time**: 133.06s (2:13) - performance concerns
- **Failure categories**: CLI, Integration, ADK Agents, Prompts

### Test Failure Categories

#### 1. CLI E2E Test Failures (8 failures)
- **Issue**: Mock setup problems, missing CLI options, output assertions
- **Root Cause**: Tests expect different behavior than implementation
- **Priority**: HIGH - Core user functionality

#### 2. Integration Test Failures (2 failures)  
- **Issue**: Mock object subscriptability, variable scope
- **Root Cause**: Incorrect mocking patterns
- **Priority**: HIGH - Workflow orchestration

#### 3. ADK Agent Test Failures (2 failures)
- **Issue**: Pydantic validation errors, attribute access
- **Root Cause**: Google ADK integration issues
- **Priority**: CRITICAL - Core architecture

#### 4. Prompt Test Failures (9 failures)
- **Issue**: String assertion mismatches
- **Root Cause**: Prompt template content doesn't match test expectations
- **Priority**: MEDIUM - Content validation

### Dependencies
- Google ADK framework integration
- LM Studio API mocking
- Click CLI framework
- Pytest testing framework

### Integration Points
- CLI interface with orchestrator
- ADK agents with LM Studio client
- Test mocking with external dependencies

## Constitution Check

### Gate 1: Technical Feasibility ✅
- All failures are fixable with code changes
- No fundamental architecture changes needed
- Existing test framework is adequate

### Gate 2: Scope Management ✅
- Clear categorization of failures
- Prioritized by impact and complexity
- Incremental fix approach planned

### Gate 3: Risk Assessment ✅
- Low risk - test fixes don't affect production code
- Rollback possible at any stage
- No external dependencies at risk

## Phase 0: Research & Analysis

### Research Tasks

1. **ADK Integration Issues**
   - Task: Research Google ADK SequentialAgent validation requirements
   - Context: Fix pydantic validation errors in agent initialization
   - Priority: CRITICAL

2. **CLI Mocking Patterns**
   - Task: Research best practices for Click CLI testing with mocks
   - Context: Fix CLI E2E test failures
   - Priority: HIGH

3. **Prompt Template Standards**
   - Task: Research prompt engineering best practices for AI agents
   - Context: Align prompt content with test expectations
   - Priority: MEDIUM

### Research Findings

**ADK Integration**:
- SequentialAgent requires specific parameter validation
- Sub-agents must be properly initialized before workflow creation
- Error handling needs improvement for missing dependencies

**CLI Testing**:
- Click testing requires proper mock setup for external dependencies
- Output assertions need to match actual CLI behavior
- Legacy mode option needs to be added to CLI interface

**Prompt Engineering**:
- Prompts should include specific keywords for test validation
- Content structure should match expected patterns
- Template variables need proper formatting

## Phase 1: Design & Implementation

### Data Model Updates

**TestResult Entity**:
- test_name: string
- status: enum (PASS, FAIL, SKIP)
- error_message: string (optional)
- execution_time: float
- category: enum (CLI, INTEGRATION, ADK, PROMPTS)

**FixPlan Entity**:
- category: string
- priority: enum (CRITICAL, HIGH, MEDIUM, LOW)
- estimated_effort: integer (hours)
- dependencies: array of strings
- status: enum (PENDING, IN_PROGRESS, COMPLETED)

### API Contracts

**Test Fix Endpoints**:
- `POST /api/test-fixes/validate` - Validate fix approach
- `POST /api/test-fixes/apply` - Apply specific fixes
- `GET /api/test-fixes/status` - Get fix progress

### Implementation Strategy

#### Phase 1A: Critical Fixes (ADK Agents)
1. Fix SequentialAgent validation errors
2. Resolve attribute access issues
3. Update agent initialization patterns

#### Phase 1B: High Priority Fixes (CLI & Integration)
1. Fix CLI mock setup issues
2. Add missing CLI options (--legacy)
3. Resolve integration test mocking

#### Phase 1C: Medium Priority Fixes (Prompts)
1. Update prompt templates to match test expectations
2. Add missing keywords and content
3. Validate prompt structure

### Quick Start Guide

**For Developers**:
1. Run `uv run python -m pytest tests/unit/` to verify unit test fixes
2. Run `uv run python -m pytest tests/integration/` to verify integration fixes  
3. Run `uv run python -m pytest tests/e2e/` to verify E2E fixes
4. Run full test suite to confirm all fixes

**For Testers**:
1. Execute specific test categories to validate fixes
2. Check test execution time improvements
3. Verify no regression in passing tests

## Phase 2: Implementation Execution

### Step-by-Step Fix Plan

#### Step 1: Fix ADK Agent Issues (CRITICAL)
- **Files**: `src/agents/orchestrator.py`, `tests/test_adk_agents.py`
- **Actions**:
  - Fix SequentialAgent parameter validation
  - Resolve attribute access errors
  - Update agent initialization
- **Validation**: Run ADK agent tests

#### Step 2: Fix CLI E2E Tests (HIGH)
- **Files**: `src/essay_composer.py`, `tests/e2e/test_cli_e2e.py`
- **Actions**:
  - Add missing --legacy CLI option
  - Fix mock setup for CLI tests
  - Update output assertions
- **Validation**: Run CLI E2E tests

#### Step 3: Fix Integration Tests (HIGH)
- **Files**: `tests/integration/test_agent_integration.py`
- **Actions**:
  - Fix mock object subscriptability
  - Resolve variable scope issues
  - Update integration test patterns
- **Validation**: Run integration tests

#### Step 4: Fix Prompt Tests (MEDIUM)
- **Files**: `src/prompts.py`, `tests/test_prompts.py`, `tests/unit/test_prompts_unit.py`
- **Actions**:
  - Update prompt templates with expected content
  - Add missing keywords
  - Validate prompt structure
- **Validation**: Run prompt tests

#### Step 5: Performance Optimization
- **Actions**:
  - Optimize test execution time
  - Reduce mock overhead
  - Improve test parallelization
- **Validation**: Measure test execution time

### Success Metrics

1. **Test Pass Rate**: 100% of tests passing (81/81)
2. **Execution Time**: < 60 seconds for full test suite
3. **Code Coverage**: Maintain or improve current coverage
4. **Regression Prevention**: No new test failures introduced

### Risk Mitigation

1. **Incremental Fixes**: Fix one category at a time
2. **Validation**: Run tests after each fix
3. **Rollback**: Git commit after each successful fix
4. **Documentation**: Update test documentation as needed

## Next Steps

1. **Immediate**: Start with ADK agent fixes (CRITICAL)
2. **Short-term**: Complete CLI and integration fixes (HIGH)
3. **Medium-term**: Address prompt test fixes (MEDIUM)
4. **Long-term**: Performance optimization and test maintenance

This plan provides a systematic approach to fixing all 21 test failures while maintaining code quality and preventing regressions.
