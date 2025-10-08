"""
Reflector Agent using Google ADK.
"""
from google.adk.agents import LlmAgent
from typing import Dict, Any
from llm_client import LMStudioClient
from prompts import EssayPrompts


class ReflectorAgent:
    """ADK Agent for reflecting on and critiquing essay drafts."""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234/v1"):
        """Initialize the reflector agent.
        
        Args:
            lm_studio_url: LM Studio API endpoint
        """
        self.client = LMStudioClient(lm_studio_url)
        self.prompts = EssayPrompts()
        
        # Create the ADK LlmAgent
        self.adk_agent = LlmAgent(
            name="ReflectorAgent",
            model="openai/gpt-oss-20b",
            instruction="""You are an expert essay reviewer. Provide a detailed critique of the following essay.

Focus on:
1. **Structure and Organization**: Is the essay well-organized with clear introduction, body, and conclusion?
2. **Argument Quality**: Are the arguments logical, well-supported, and persuasive?
3. **Clarity and Coherence**: Is the writing clear and easy to follow?
4. **Evidence and Examples**: Are claims supported with appropriate evidence?
5. **Writing Quality**: Grammar, style, and flow
6. **Areas for Improvement**: Specific suggestions for enhancement

Essay to critique:
{draft}

Critique:""",
            description="Reflects on and critiques essay drafts to identify areas for improvement",
            output_key="critique"
        )
    
    def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on and critique the essay draft.
        
        Args:
            context: Context containing the essay draft
            
        Returns:
            Updated context with the critique
        """
        draft = context.get("draft", "")
        if not draft:
            raise ValueError("Draft is required for reflection")
        
        # Generate critique
        critique_prompt = self.prompts.get_reflector_prompt(draft)
        critique = self.client.generate_text(critique_prompt)
        
        # Update context with the critique
        context["critique"] = critique
        context["reflection_status"] = "completed"
        
        return context
    
    def get_description(self) -> str:
        """Get agent description."""
        return "Reflects on and critiques essay drafts to identify areas for improvement"
