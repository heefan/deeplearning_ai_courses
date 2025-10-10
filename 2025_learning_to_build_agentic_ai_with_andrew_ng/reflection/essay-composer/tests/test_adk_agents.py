"""
Tests for ADK agent integration.
"""
import pytest
from unittest.mock import Mock, patch
from src.agents.essay_generator import EssayGeneratorAgent
from src.agents.reflector import ReflectorAgent
from src.agents.reviser import ReviserAgent
from src.agents.orchestrator import EssayComposerOrchestrator


class TestEssayGeneratorAgent:
    """Test cases for EssayGeneratorAgent."""
    
    @patch('src.agents.essay_generator.LMStudioClient')
    def test_init(self, mock_client_class):
        """Test agent initialization."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = EssayGeneratorAgent("http://test:8080/v1")
        
        assert agent.client == mock_client
        mock_client_class.assert_called_once_with("http://test:8080/v1")
    
    @patch('src.agents.essay_generator.LMStudioClient')
    def test_execute_success(self, mock_client_class):
        """Test successful essay generation."""
        mock_client = Mock()
        mock_client.generate_text.return_value = "Generated essay draft"
        mock_client_class.return_value = mock_client
        
        agent = EssayGeneratorAgent()
        context = {"topic": "Test Topic"}
        
        result = agent.run_async(context)
        
        assert result["draft"] == "Generated essay draft"
        assert result["generation_status"] == "completed"
        assert result["topic"] == "Test Topic"
    
    @patch('src.agents.essay_generator.LMStudioClient')
    def test_execute_missing_topic(self, mock_client_class):
        """Test execution with missing topic."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = EssayGeneratorAgent()
        context = {}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Topic is required" in str(exc_info.value)


class TestReflectorAgent:
    """Test cases for ReflectorAgent."""
    
    @patch('src.agents.reflector.LMStudioClient')
    def test_execute_success(self, mock_client_class):
        """Test successful reflection."""
        mock_client = Mock()
        mock_client.generate_text.return_value = "Critique feedback"
        mock_client_class.return_value = mock_client
        
        agent = ReflectorAgent()
        context = {"draft": "Test draft"}
        
        result = agent.run_async(context)
        
        assert result["critique"] == "Critique feedback"
        assert result["reflection_status"] == "completed"
        assert result["draft"] == "Test draft"
    
    @patch('src.agents.reflector.LMStudioClient')
    def test_execute_missing_draft(self, mock_client_class):
        """Test execution with missing draft."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReflectorAgent()
        context = {}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Draft is required" in str(exc_info.value)


class TestReviserAgent:
    """Test cases for ReviserAgent."""
    
    @patch('src.agents.reviser.LMStudioClient')
    def test_execute_success(self, mock_client_class):
        """Test successful revision."""
        mock_client = Mock()
        mock_client.generate_text.return_value = "Final essay"
        mock_client_class.return_value = mock_client
        
        agent = ReviserAgent()
        context = {"draft": "Test draft", "critique": "Test critique"}
        
        result = agent.run_async(context)
        
        assert result["final_essay"] == "Final essay"
        assert result["revision_status"] == "completed"
        assert result["workflow_status"] == "completed"
    
    @patch('src.agents.reviser.LMStudioClient')
    def test_execute_missing_inputs(self, mock_client_class):
        """Test execution with missing draft or critique."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReviserAgent()
        
        # Test missing draft
        context = {"critique": "Test critique"}
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        assert "Both draft and critique are required" in str(exc_info.value)
        
        # Test missing critique
        context = {"draft": "Test draft"}
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        assert "Both draft and critique are required" in str(exc_info.value)


class TestEssayComposerOrchestrator:
    """Test cases for EssayComposerOrchestrator."""
    
    @patch('src.agents.orchestrator.EssayGeneratorAgent')
    @patch('src.agents.orchestrator.ReflectorAgent')
    @patch('src.agents.orchestrator.ReviserAgent')
    def test_init(self, mock_reviser, mock_reflector, mock_generator):
        """Test orchestrator initialization."""
        mock_gen_instance = Mock()
        mock_ref_instance = Mock()
        mock_rev_instance = Mock()
        
        # Create mock adk_agent attributes for each agent
        mock_gen_instance.adk_agent = Mock()
        mock_ref_instance.adk_agent = Mock()
        mock_rev_instance.adk_agent = Mock()
        
        mock_generator.return_value = mock_gen_instance
        mock_reflector.return_value = mock_ref_instance
        mock_reviser.return_value = mock_rev_instance
        
        orchestrator = EssayComposerOrchestrator("http://test:8080/v1")
        
        assert orchestrator.generator == mock_gen_instance
        assert orchestrator.reflector == mock_ref_instance
        assert orchestrator.reviser == mock_rev_instance
        # During testing with mocks, workflow should be None
        assert orchestrator.workflow is None
    
    def test_get_workflow_info(self):
        """Test workflow info retrieval."""
        orchestrator = EssayComposerOrchestrator()
        orchestrator.generator = Mock()
        orchestrator.reflector = Mock()
        orchestrator.reviser = Mock()
        
        orchestrator.generator.get_description.return_value = "Generator description"
        orchestrator.reflector.get_description.return_value = "Reflector description"
        orchestrator.reviser.get_description.return_value = "Reviser description"
        
        info = orchestrator.get_workflow_info()
        
        assert info["generator"] == "Generator description"
        assert info["reflector"] == "Reflector description"
        assert info["reviser"] == "Reviser description"
        assert info["workflow_type"] == "SequentialAgent ADK Workflow"
