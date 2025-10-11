"""
Orchestrator for managing the reflection loop between generator and critic agents.

This component implements the reflection AI design pattern by coordinating
the generator-critic cycle for iterative code improvement.
"""

from typing import Dict, Any, Optional, List
import asyncio
from dataclasses import dataclass
from datetime import datetime

from .generator import GeneratorAgent, GeneratorResponse
from .critic import CriticAgent, CritiqueResponse, CritiqueResult
from ..executor.code_executor import CodeExecutor, ExecutionResult


@dataclass
class ReflectionResult:
    """Result of the reflection process."""
    final_code: str
    iterations: int
    execution_result: Optional[ExecutionResult]
    history: List[Dict[str, Any]]
    success: bool
    error_message: Optional[str] = None


class ReflectionOrchestrator:
    """
    Orchestrates the reflection loop between generator and critic agents.
    
    This class manages the iterative process of:
    1. Generate code with GeneratorAgent
    2. Critique code with CriticAgent
    3. If approved: execute and return
    4. If not approved: regenerate with feedback
    5. Repeat up to max iterations
    """
    
    def __init__(
        self,
        generator: GeneratorAgent,
        critic: CriticAgent,
        executor: CodeExecutor,
        max_iterations: int = 3
    ):
        """
        Initialize the reflection orchestrator.
        
        Args:
            generator: Generator agent for creating code
            critic: Critic agent for reviewing code
            executor: Code executor for testing generated code
            max_iterations: Maximum number of reflection iterations
        """
        self.generator = generator
        self.critic = critic
        self.executor = executor
        self.max_iterations = max_iterations
    
    async def reflect_and_generate(
        self,
        user_query: str,
        execute_code: bool = True
    ) -> ReflectionResult:
        """
        Execute the reflection loop to generate and improve code.
        
        Args:
            user_query: The user's request for chart generation
            execute_code: Whether to execute the final code for validation
            
        Returns:
            ReflectionResult containing the final code and process history
        """
        history = []
        context = {}
        
        try:
            for iteration in range(self.max_iterations):
                # Generate code
                generator_response = await self.generator.generate_code(
                    user_query, context
                )
                
                # Critique the generated code
                critique_response = await self.critic.critique_code(
                    generator_response.code,
                    user_query,
                    context
                )
                
                # Record this iteration
                iteration_record = {
                    "iteration": iteration + 1,
                    "timestamp": datetime.now().isoformat(),
                    "generator_response": {
                        "code": generator_response.code,
                        "explanation": generator_response.explanation,
                        "confidence": generator_response.confidence
                    },
                    "critique_response": {
                        "result": critique_response.result.value,
                        "feedback": critique_response.feedback,
                        "suggestions": critique_response.suggestions,
                        "confidence": critique_response.confidence,
                        "issues": critique_response.issues
                    }
                }
                history.append(iteration_record)
                
                # Check if code is approved
                if critique_response.result == CritiqueResult.APPROVED:
                    # Code is approved, optionally execute it
                    execution_result = None
                    if execute_code:
                        try:
                            execution_result = await self.executor.execute_code(
                                generator_response.code
                            )
                        except Exception as e:
                            # Execution failed, but code was approved
                            # This might indicate a critic issue
                            iteration_record["execution_error"] = str(e)
                    
                    return ReflectionResult(
                        final_code=generator_response.code,
                        iterations=iteration + 1,
                        execution_result=execution_result,
                        history=history,
                        success=True
                    )
                
                # Code needs improvement, update context for next iteration
                context["previous_attempts"] = context.get("previous_attempts", [])
                context["previous_attempts"].append({
                    "code": generator_response.code,
                    "feedback": critique_response.feedback,
                    "suggestions": critique_response.suggestions
                })
                
                context["previous_critiques"] = context.get("previous_critiques", [])
                context["previous_critiques"].append({
                    "feedback": critique_response.feedback,
                    "suggestions": critique_response.suggestions,
                    "issues": critique_response.issues
                })
            
            # Max iterations reached without approval
            return ReflectionResult(
                final_code=generator_response.code,
                iterations=self.max_iterations,
                execution_result=None,
                history=history,
                success=False,
                error_message="Maximum iterations reached without approval"
            )
            
        except Exception as e:
            return ReflectionResult(
                final_code="",
                iterations=len(history),
                execution_result=None,
                history=history,
                success=False,
                error_message=f"Reflection process failed: {str(e)}"
            )
    
    async def close(self) -> None:
        """Close all agents and clean up resources."""
        await asyncio.gather(
            self.generator.close(),
            self.critic.close(),
            return_exceptions=True
        )
