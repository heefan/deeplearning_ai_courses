"""
Essay Generator Agent using Google ADK.
"""
from google.adk.agents import LlmAgent
from typing import Dict, Any
from ..llm_client import LMStudioClient
from ..prompts import EssayPrompts


class EssayGeneratorAgent:
    """ADK Agent for generating initial essay drafts."""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234/v1"):
        """Initialize the essay generator agent.
        
        Args:
            lm_studio_url: LM Studio API endpoint
        """
        self.client = LMStudioClient(lm_studio_url)
        self.prompts = EssayPrompts()
        
        # Create the ADK LlmAgent
        self.adk_agent = LlmAgent(
            name="EssayGeneratorAgent",
            model="openai/gpt-oss-20b",
            instruction="""You are an expert essay writer. Write a well-structured essay on the given topic.
            
Requirements:
- Write a complete essay with introduction, body paragraphs, and conclusion
- Aim for 500-800 words
- Use clear, coherent arguments
- Include specific examples or evidence where appropriate
- Write in a formal, academic tone

Topic: {topic}

Essay:""",
            description="Generates initial essay drafts based on the given topic",
            output_key="draft"
        )
    
    def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an initial essay draft.
        
        Args:
            context: Context containing the essay topic
            
        Returns:
            Updated context with the generated draft
        """
        topic = context.get("topic", "")
        if not topic:
            raise ValueError("Topic is required for essay generation")
        
        # Generate the initial draft
        draft_prompt = self.prompts.get_generator_prompt(topic)
        draft = self.client.generate_text(draft_prompt)
        
        # Update context with the draft
        context["draft"] = draft
        context["generation_status"] = "completed"
        
        return context
    
    def get_description(self) -> str:
        """Get agent description."""
        return "Generates initial essay drafts based on the given topic"
