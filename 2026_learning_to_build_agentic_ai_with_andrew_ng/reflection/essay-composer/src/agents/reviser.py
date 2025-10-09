"""
Reviser Agent using Google ADK.
"""
from google.adk.agents import LlmAgent
from typing import Dict, Any
from ..llm_client import LMStudioClient
from ..prompts import EssayPrompts


class ReviserAgent:
    """ADK Agent for revising essays based on critique."""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234/v1"):
        """Initialize the reviser agent.
        
        Args:
            lm_studio_url: LM Studio API endpoint
        """
        self.client = LMStudioClient(lm_studio_url)
        self.prompts = EssayPrompts()
        
        # Create the ADK LlmAgent
        self.adk_agent = LlmAgent(
            name="ReviserAgent",
            model="openai/gpt-oss-20b",
            instruction="""You are an expert essay editor. Based on the following essay draft and critique, write an improved version of the essay.

Original Essay:
{draft}

Critique and Feedback:
{critique}

Please revise the essay incorporating the feedback. Maintain the same topic and core arguments while addressing the identified issues. Write a polished, final version that is well-structured, clear, and persuasive.

Revised Essay:""",
            description="Revises essays based on critique to produce the final polished version",
            output_key="final_essay"
        )
    
    def run_async(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Revise the essay based on critique.
        
        Args:
            context: Context containing the draft and critique
            
        Returns:
            Updated context with the final essay
        """
        draft = context.get("draft", "")
        critique = context.get("critique", "")
        
        if not draft or not critique:
            raise ValueError("Both draft and critique are required for revision")
        
        # Generate final essay
        revision_prompt = self.prompts.get_revision_prompt(draft, critique)
        final_essay = self.client.generate_text(revision_prompt)
        
        # Update context with the final essay
        context["final_essay"] = final_essay
        context["revision_status"] = "completed"
        context["workflow_status"] = "completed"
        
        return context
    
    def get_description(self) -> str:
        """Get agent description."""
        return "Revises essays based on critique to produce the final polished version"
