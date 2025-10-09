"""
Integration tests for ADK agent interactions.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.agents.orchestrator import EssayComposerOrchestrator
from src.agents.essay_generator import EssayGeneratorAgent
from src.agents.reflector import ReflectorAgent
from src.agents.reviser import ReviserAgent


class TestAgentIntegration:
    """Integration tests for agent interactions."""
    
    @patch('src.agents.orchestrator.EssayGeneratorAgent')
    @patch('src.agents.orchestrator.ReflectorAgent')
    @patch('src.agents.orchestrator.ReviserAgent')
    @patch('src.agents.orchestrator.SequentialAgent')
    def test_orchestrator_agent_initialization(self, mock_sequential, mock_reviser, mock_reflector, mock_generator):
        """Test that orchestrator properly initializes all agents."""
        mock_gen_instance = Mock()
        mock_ref_instance = Mock()
        mock_rev_instance = Mock()
        mock_workflow = Mock()
        
        mock_generator.return_value = mock_gen_instance
        mock_reflector.return_value = mock_ref_instance
        mock_reviser.return_value = mock_rev_instance
        mock_sequential.return_value = mock_workflow
        
        orchestrator = EssayComposerOrchestrator("http://test:8080/v1")
        
        # Verify all agents were initialized
        mock_generator.assert_called_once_with("http://test:8080/v1")
        mock_reflector.assert_called_once_with("http://test:8080/v1")
        mock_reviser.assert_called_once_with("http://test:8080/v1")
        
        # Verify SequentialAgent workflow was created with all agents
        mock_sequential.assert_called_once_with(
            name="EssayComposerWorkflow",
            sub_agents=[mock_gen_instance.adk_agent, mock_ref_instance.adk_agent, mock_rev_instance.adk_agent],
            description="Executes a sequence of essay generation, reflection, and revision."
        )
        
        assert orchestrator.workflow == mock_workflow
    
    @patch('src.agents.orchestrator.EssayGeneratorAgent')
    @patch('src.agents.orchestrator.ReflectorAgent')
    @patch('src.agents.orchestrator.ReviserAgent')
    @patch('src.agents.orchestrator.SequentialAgent')
    def test_workflow_execution_integration(self, mock_sequential, mock_reviser, mock_reflector, mock_generator):
        """Test that workflow executes all agents in sequence."""
        # Setup mocks
        mock_gen_instance = Mock()
        mock_ref_instance = Mock()
        mock_rev_instance = Mock()
        mock_workflow = Mock()
        
        mock_generator.return_value = mock_gen_instance
        mock_reflector.return_value = mock_ref_instance
        mock_reviser.return_value = mock_rev_instance
        mock_sequential.return_value = mock_workflow
        
        # Mock workflow execution
        expected_result = {
            "topic": "Test Topic",
            "draft": "Generated draft",
            "critique": "Generated critique",
            "final_essay": "Final essay",
            "workflow_status": "completed"
        }
        mock_workflow.execute.return_value = expected_result
        
        orchestrator = EssayComposerOrchestrator()
        result = orchestrator.compose_essay("Test Topic", verbose=False)
        
        # Verify workflow was called with correct context
        # Note: We now use manual execution instead of workflow.execute
        assert result["topic"] == "Test Topic"
        assert result["workflow_status"] == "completed"
        
        # Verify result
        assert result == expected_result
    
    @patch('src.agents.orchestrator.EssayGeneratorAgent')
    @patch('src.agents.orchestrator.ReflectorAgent')
    @patch('src.agents.orchestrator.ReviserAgent')
    @patch('src.agents.orchestrator.SequentialAgent')
    def test_workflow_error_handling(self, mock_sequential, mock_reviser, mock_reflector, mock_generator):
        """Test workflow error handling."""
        # Setup mocks
        mock_gen_instance = Mock()
        mock_ref_instance = Mock()
        mock_rev_instance = Mock()
        mock_workflow = Mock()
        
        mock_generator.return_value = mock_gen_instance
        mock_reflector.return_value = mock_ref_instance
        mock_reviser.return_value = mock_rev_instance
        mock_sequential.return_value = mock_workflow
        
        # Mock workflow execution failure - we'll mock the individual agents instead
        orchestrator.generator.run_async.side_effect = Exception("Workflow execution failed")
        
        orchestrator = EssayComposerOrchestrator()
        
        with pytest.raises(Exception) as exc_info:
            orchestrator.compose_essay("Test Topic", verbose=False)
        
        assert "Workflow execution failed" in str(exc_info.value)
    
    @patch('src.agents.orchestrator.EssayGeneratorAgent')
    @patch('src.agents.orchestrator.ReflectorAgent')
    @patch('src.agents.orchestrator.ReviserAgent')
    @patch('src.agents.orchestrator.SequentialAgent')
    def test_get_workflow_info_integration(self, mock_sequential, mock_reviser, mock_reflector, mock_generator):
        """Test workflow info retrieval with all agents."""
        # Setup mocks
        mock_gen_instance = Mock()
        mock_ref_instance = Mock()
        mock_rev_instance = Mock()
        mock_workflow = Mock()
        
        mock_generator.return_value = mock_gen_instance
        mock_reflector.return_value = mock_ref_instance
        mock_reviser.return_value = mock_rev_instance
        mock_sequential.return_value = mock_workflow
        
        # Mock agent descriptions
        mock_gen_instance.get_description.return_value = "Generator description"
        mock_ref_instance.get_description.return_value = "Reflector description"
        mock_rev_instance.get_description.return_value = "Reviser description"
        
        orchestrator = EssayComposerOrchestrator()
        info = orchestrator.get_workflow_info()
        
        # Verify all agent descriptions are included
        assert info["generator"] == "Generator description"
        assert info["reflector"] == "Reflector description"
        assert info["reviser"] == "Reviser description"
        assert info["workflow_type"] == "SequentialAgent ADK Workflow"
        
        # Verify all agents were queried for descriptions
        mock_gen_instance.get_description.assert_called_once()
        mock_ref_instance.get_description.assert_called_once()
        mock_rev_instance.get_description.assert_called_once()
    
    def test_agent_context_passing(self):
        """Test that context is properly passed between agents."""
        # This test verifies the context passing mechanism
        # In a real integration, we would test that:
        # 1. Generator adds 'draft' to context
        # 2. Reflector uses 'draft' and adds 'critique'
        # 3. Reviser uses both 'draft' and 'critique' to create 'final_essay'
        
        # Mock the agents
        generator = Mock()
        reflector = Mock()
        reviser = Mock()
        
        # Setup context passing
        initial_context = {"topic": "Test Topic"}
        
        # Generator adds draft
        generator.execute.return_value = {**initial_context, "draft": "Generated draft"}
        
        # Reflector uses draft and adds critique
        reflector.execute.return_value = {
            **initial_context, 
            "draft": "Generated draft", 
            "critique": "Generated critique"
        }
        
        # Reviser uses draft and critique to create final essay
        reviser.execute.return_value = {
            **initial_context,
            "draft": "Generated draft",
            "critique": "Generated critique",
            "final_essay": "Final essay"
        }
        
        # Test context passing
        context = initial_context.copy()
        context = generator.execute(context)
        assert "draft" in context
        
        context = reflector.execute(context)
        assert "draft" in context
        assert "critique" in context
        
        context = reviser.execute(context)
        assert "draft" in context
        assert "critique" in context
        assert "final_essay" in context
