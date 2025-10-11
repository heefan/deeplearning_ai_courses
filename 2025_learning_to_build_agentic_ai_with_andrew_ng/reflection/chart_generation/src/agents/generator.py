"""
Generator Agent for creating Python chart code.

This agent uses ADK to generate matplotlib code based on user queries
and the coffee sales dataset schema.
"""

from typing import Dict, Any, Optional
import asyncio
from dataclasses import dataclass

from google.adk import Agent, AgentConfig
from google.adk.models import ModelConfig

from ..utils.data_schema import DataSchema
from ..utils.prompt_templates import GENERATOR_PROMPT_TEMPLATE


@dataclass
class GeneratorResponse:
    """Response from the generator agent."""
    code: str
    explanation: str
    confidence: float


class GeneratorAgent:
    """
    ADK agent that generates Python matplotlib code based on user queries.
    
    This agent takes a user query and data schema, then generates Python code
    wrapped in <execute_python> tags for safe execution.
    """
    
    def __init__(
        self,
        model_config: ModelConfig,
        data_schema: DataSchema,
        max_retries: int = 3
    ):
        """
        Initialize the generator agent.
        
        Args:
            model_config: ADK model configuration for LMStudio
            data_schema: Schema of the coffee sales dataset
            max_retries: Maximum number of retry attempts
        """
        self.model_config = model_config
        self.data_schema = data_schema
        self.max_retries = max_retries
        self._agent: Optional[Agent] = None
    
    async def _initialize_agent(self) -> None:
        """Initialize the ADK agent if not already done."""
        if self._agent is None:
            agent_config = AgentConfig(
                model_config=self.model_config,
                system_prompt=self._build_system_prompt(),
                structured_output=True
            )
            self._agent = Agent(agent_config)
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the generator agent."""
        return GENERATOR_PROMPT_TEMPLATE.format(
            schema_description=self.data_schema.get_description(),
            available_columns=", ".join(self.data_schema.columns),
            sample_data=self.data_schema.get_sample_data()
        )
    
    async def generate_code(
        self,
        user_query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> GeneratorResponse:
        """
        Generate Python chart code based on user query.
        
        Args:
            user_query: The user's request for chart generation
            context: Optional context for the generation (e.g., previous attempts)
            
        Returns:
            GeneratorResponse containing the generated code and metadata
            
        Raises:
            RuntimeError: If agent fails to generate code after retries
        """
        await self._initialize_agent()
        
        if context is None:
            context = {}
        
        prompt = self._build_user_prompt(user_query, context)
        
        for attempt in range(self.max_retries):
            try:
                response = await self._agent.generate(
                    prompt=prompt,
                    structured_output=True
                )
                
                # Parse the structured response
                return self._parse_response(response)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        f"Generator agent failed after {self.max_retries} attempts: {e}"
                    )
                await asyncio.sleep(1)  # Brief delay before retry
        
        raise RuntimeError("Generator agent failed unexpectedly")
    
    def _build_user_prompt(self, user_query: str, context: Dict[str, Any]) -> str:
        """Build the user prompt for code generation."""
        prompt = f"User Query: {user_query}\n\n"
        
        if context.get("previous_attempts"):
            prompt += "Previous attempts and feedback:\n"
            for i, attempt in enumerate(context["previous_attempts"], 1):
                prompt += f"Attempt {i}: {attempt.get('code', 'N/A')}\n"
                prompt += f"Feedback: {attempt.get('feedback', 'N/A')}\n\n"
        
        prompt += "Please generate Python matplotlib code to fulfill this request."
        return prompt
    
    def _parse_response(self, response: Dict[str, Any]) -> GeneratorResponse:
        """Parse the structured response from the agent."""
        try:
            code = response.get("code", "")
            explanation = response.get("explanation", "")
            confidence = float(response.get("confidence", 0.0))
            
            # Ensure code is wrapped in execute_python tags
            if not code.strip().startswith("<execute_python>"):
                code = f"<execute_python>\n{code}\n</execute_python>"
            
            return GeneratorResponse(
                code=code,
                explanation=explanation,
                confidence=confidence
            )
            
        except (KeyError, ValueError, TypeError) as e:
            raise RuntimeError(f"Failed to parse generator response: {e}")
    
    async def close(self) -> None:
        """Close the agent and clean up resources."""
        if self._agent:
            await self._agent.close()
            self._agent = None
