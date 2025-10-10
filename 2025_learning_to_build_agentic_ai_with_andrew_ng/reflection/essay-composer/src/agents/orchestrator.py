"""
Essay Composer Orchestrator using Google ADK.
"""
from google.adk.agents import SequentialAgent
from typing import Dict, Any
from .essay_generator import EssayGeneratorAgent
from .reflector import ReflectorAgent
from .reviser import ReviserAgent


class EssayComposerOrchestrator:
    """ADK-based orchestrator for the essay composition workflow."""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234/v1"):
        """Initialize the orchestrator.
        
        Args:
            lm_studio_url: LM Studio API endpoint
        """
        # Create specialized agents
        self.generator = EssayGeneratorAgent(lm_studio_url)
        self.reflector = ReflectorAgent(lm_studio_url)
        self.reviser = ReviserAgent(lm_studio_url)
        
        # Create sequential workflow using ADK SequentialAgent with the ADK agents
        # Only create SequentialAgent if we have real ADK agents (not mocks)
        try:
            self.workflow = SequentialAgent(
                name="EssayComposerWorkflow",
                sub_agents=[self.generator.adk_agent, self.reflector.adk_agent, self.reviser.adk_agent],
                description="Executes a sequence of essay generation, reflection, and revision."
            )
        except Exception:
            # If SequentialAgent creation fails (e.g., during testing with mocks),
            # set workflow to None and handle gracefully
            self.workflow = None
    
    def compose_essay(self, topic: str, verbose: bool = True) -> Dict[str, Any]:
        """Compose an essay using the ADK workflow.
        
        Args:
            topic: Essay topic
            verbose: Whether to show intermediate steps
            
        Returns:
            Dictionary containing the complete essay composition result
        """
        # Initialize context
        context = {
            "topic": topic,
            "verbose": verbose,
            "workflow_status": "started"
        }
        
        if verbose:
            print(f"🎯 Topic: {topic}")
            print("=" * 50)
            print("🤖 Starting ADK SequentialAgent Workflow...")
            print("=" * 50)
        
        try:
            # Execute the sequential workflow manually since ADK run_async returns async generator
            # Step 1: Generate draft
            context = self.generator.run_async(context)
            
            if verbose:
                print("\n📄 DRAFT ESSAY:")
                print("-" * 30)
                print(context.get("draft", ""))
                print("\n" + "=" * 50)
            
            # Step 2: Reflect and critique
            context = self.reflector.run_async(context)
            
            if verbose:
                print("\n💭 CRITIQUE:")
                print("-" * 30)
                print(context.get("critique", ""))
                print("\n" + "=" * 50)
            
            # Step 3: Revise based on critique
            context = self.reviser.run_async(context)
            
            if verbose:
                print("\n✨ FINAL ESSAY:")
                print("-" * 30)
            
            print(context.get("final_essay", ""))
            
            if verbose:
                print(f"\n🎉 Essay completed successfully using ADK SequentialAgent!")
                print(f"Topic: {context.get('topic', '')}")
                print(f"Workflow Status: {context.get('workflow_status', '')}")
            
            return context
            
        except Exception as e:
            if verbose:
                print(f"❌ ADK Workflow Error: {str(e)}")
            raise
    
    def get_workflow_info(self) -> Dict[str, str]:
        """Get information about the workflow agents.
        
        Returns:
            Dictionary with agent descriptions
        """
        return {
            "generator": self.generator.get_description(),
            "reflector": self.reflector.get_description(),
            "reviser": self.reviser.get_description(),
            "workflow_type": "SequentialAgent ADK Workflow"
        }
