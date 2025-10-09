# Quick Start Guide: Test Fix Implementation

**Feature**: Check Feature  
**Created**: 2024-12-19  
**Status**: Ready for Implementation  

## Overview

This guide provides step-by-step instructions for fixing the 21 failing tests in the Essay Composer project. The fixes are organized by priority and category to ensure systematic resolution.

## Prerequisites

- Python 3.9+ with uv package manager
- Access to the Essay Composer codebase
- Understanding of pytest testing framework
- Basic knowledge of Google ADK and Click CLI

## Quick Start Steps

### 1. Environment Setup

```bash
# Navigate to project directory
cd /Users/litian/dreamworks/deeplearning_ai_courses/2026_learning_to_build_agentic_ai_with_andrew_ng/reflection/essay-composer

# Install dependencies
uv sync

# Verify current test status
uv run python -m pytest --tb=short
```

### 2. Critical Fixes (ADK Agents) - Start Here

**Priority**: CRITICAL  
**Estimated Time**: 2-3 hours  
**Files**: `src/agents/orchestrator.py`, `tests/test_adk_agents.py`

#### Step 2.1: Fix SequentialAgent Validation
```bash
# Run ADK agent tests to see current errors
uv run python -m pytest tests/test_adk_agents.py -v
```

**Issues to fix**:
- Pydantic validation errors for SequentialAgent
- Attribute access errors in orchestrator
- Agent initialization problems

**Implementation**:
1. Review Google ADK documentation for SequentialAgent usage
2. Fix parameter types and validation in orchestrator
3. Add proper error handling for missing dependencies
4. Update agent initialization patterns

#### Step 2.2: Verify ADK Fixes
```bash
# Test ADK agent fixes
uv run python -m pytest tests/test_adk_agents.py -v
```

### 3. High Priority Fixes (CLI & Integration)

**Priority**: HIGH  
**Estimated Time**: 3-4 hours  
**Files**: `src/essay_composer.py`, `tests/e2e/test_cli_e2e.py`, `tests/integration/test_agent_integration.py`

#### Step 3.1: Fix CLI Issues
```bash
# Run CLI E2E tests to see current errors
uv run python -m pytest tests/e2e/test_cli_e2e.py -v
```

**Issues to fix**:
- Missing --legacy CLI option
- Mock setup problems
- Output assertion mismatches
- Connection test failures

**Implementation**:
1. Add missing --legacy CLI option to essay_composer.py
2. Fix mock setup for external dependencies
3. Update output assertions to match actual behavior
4. Improve error handling in CLI interface

#### Step 3.2: Fix Integration Tests
```bash
# Run integration tests to see current errors
uv run python -m pytest tests/integration/test_agent_integration.py -v
```

**Issues to fix**:
- Mock object subscriptability errors
- Variable scope issues
- Workflow execution problems

**Implementation**:
1. Use MagicMock instead of Mock for subscriptable objects
2. Fix variable scope issues in test setup
3. Improve mock configuration for complex objects

#### Step 3.3: Verify High Priority Fixes
```bash
# Test CLI and integration fixes
uv run python -m pytest tests/e2e/test_cli_e2e.py tests/integration/test_agent_integration.py -v
```

### 4. Medium Priority Fixes (Prompts)

**Priority**: MEDIUM  
**Estimated Time**: 1-2 hours  
**Files**: `src/prompts.py`, `tests/test_prompts.py`, `tests/unit/test_prompts_unit.py`

#### Step 4.1: Fix Prompt Tests
```bash
# Run prompt tests to see current errors
uv run python -m pytest tests/test_prompts.py tests/unit/test_prompts_unit.py -v
```

**Issues to fix**:
- Missing keywords in prompt templates
- Content structure mismatches
- Assertion failures

**Implementation**:
1. Add missing keywords like "well-structured essay"
2. Include "Structure and Organization" in reflector prompts
3. Add "incorporating the feedback" to revision prompts
4. Validate prompt structure and content

#### Step 4.2: Verify Prompt Fixes
```bash
# Test prompt fixes
uv run python -m pytest tests/test_prompts.py tests/unit/test_prompts_unit.py -v
```

### 5. Performance Optimization

**Priority**: LOW  
**Estimated Time**: 1 hour  
**Goal**: Reduce test execution time from 133 seconds to < 60 seconds

#### Step 5.1: Optimize Test Execution
```bash
# Measure current execution time
time uv run python -m pytest
```

**Optimization strategies**:
1. Use pytest-xdist for parallel execution
2. Optimize mock setup to reduce overhead
3. Cache expensive operations in tests
4. Remove redundant test setup

#### Step 5.2: Verify Performance
```bash
# Measure optimized execution time
time uv run python -m pytest
```

## Validation Steps

### After Each Fix Category
```bash
# Run specific test category
uv run python -m pytest tests/[category]/ -v

# Check for regressions
uv run python -m pytest tests/ -x --tb=short
```

### Final Validation
```bash
# Run complete test suite
uv run python -m pytest

# Verify all tests pass
echo "Expected: 81 tests passing, 0 failures"
```

## Troubleshooting

### Common Issues

#### ADK Validation Errors
- **Problem**: Pydantic validation failures
- **Solution**: Check Google ADK documentation for correct parameter types
- **Debug**: Add logging to see actual parameter values

#### CLI Mock Issues
- **Problem**: Mocks not working as expected
- **Solution**: Use MagicMock for complex objects, check mock setup
- **Debug**: Add print statements to verify mock behavior

#### Prompt Assertion Failures
- **Problem**: String content doesn't match expectations
- **Solution**: Update prompt templates to include expected keywords
- **Debug**: Print actual prompt content to see differences

### Getting Help

1. **Check logs**: Look at test output for specific error messages
2. **Review documentation**: Consult Google ADK and Click documentation
3. **Debug step by step**: Add logging to understand execution flow
4. **Ask for help**: Document specific issues with error messages

## Success Criteria

- ✅ All 81 tests passing (currently 60 passing, 21 failing)
- ✅ Test execution time < 60 seconds (currently 133 seconds)
- ✅ No regressions in existing functionality
- ✅ All fix categories completed successfully

## Next Steps

After completing all fixes:

1. **Documentation**: Update test documentation with new patterns
2. **CI/CD**: Ensure continuous integration works with fixed tests
3. **Monitoring**: Set up test execution monitoring
4. **Maintenance**: Establish regular test maintenance procedures

## Support

For questions or issues during implementation:

1. Review the detailed implementation plan in `plan.md`
2. Check the research findings in `research.md`
3. Consult the data model in `data-model.md`
4. Review API contracts in `contracts/test-fix-api.yaml`

This quickstart guide provides a systematic approach to fixing all test failures while maintaining code quality and preventing regressions.
