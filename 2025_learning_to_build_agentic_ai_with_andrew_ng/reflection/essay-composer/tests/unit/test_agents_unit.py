"""
Unit tests for ADK agents.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.agents.essay_generator import EssayGeneratorAgent
from src.agents.reflector import ReflectorAgent
from src.agents.reviser import ReviserAgent


class TestEssayGeneratorAgentUnit:
    """Unit tests for EssayGeneratorAgent."""
    
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
        mock_client.generate_text.assert_called_once()
    
    @patch('src.agents.essay_generator.LMStudioClient')
    def test_execute_missing_topic(self, mock_client_class):
        """Test execution with missing topic."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = EssayGeneratorAgent()
        context = {}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Topic is required for essay generation" in str(exc_info.value)
    
    @patch('src.agents.essay_generator.LMStudioClient')
    def test_execute_empty_topic(self, mock_client_class):
        """Test execution with empty topic."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = EssayGeneratorAgent()
        context = {"topic": ""}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Topic is required for essay generation" in str(exc_info.value)
    
    @patch('src.agents.essay_generator.LMStudioClient')
    def test_execute_generation_error(self, mock_client_class):
        """Test execution with generation error."""
        mock_client = Mock()
        mock_client.generate_text.side_effect = Exception("Generation failed")
        mock_client_class.return_value = mock_client
        
        agent = EssayGeneratorAgent()
        context = {"topic": "Test Topic"}
        
        with pytest.raises(Exception) as exc_info:
            agent.run_async(context)
        
        assert "Generation failed" in str(exc_info.value)
    
    def test_get_description(self):
        """Test agent description."""
        agent = EssayGeneratorAgent()
        description = agent.get_description()
        
        assert isinstance(description, str)
        assert "essay" in description.lower()
        assert "draft" in description.lower()


class TestReflectorAgentUnit:
    """Unit tests for ReflectorAgent."""
    
    @patch('src.agents.reflector.LMStudioClient')
    def test_init(self, mock_client_class):
        """Test agent initialization."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReflectorAgent("http://test:8080/v1")
        
        assert agent.client == mock_client
        mock_client_class.assert_called_once_with("http://test:8080/v1")
    
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
        mock_client.generate_text.assert_called_once()
    
    @patch('src.agents.reflector.LMStudioClient')
    def test_execute_missing_draft(self, mock_client_class):
        """Test execution with missing draft."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReflectorAgent()
        context = {}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Draft is required for reflection" in str(exc_info.value)
    
    @patch('src.agents.reflector.LMStudioClient')
    def test_execute_empty_draft(self, mock_client_class):
        """Test execution with empty draft."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReflectorAgent()
        context = {"draft": ""}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Draft is required for reflection" in str(exc_info.value)
    
    @patch('src.agents.reflector.LMStudioClient')
    def test_execute_reflection_error(self, mock_client_class):
        """Test execution with reflection error."""
        mock_client = Mock()
        mock_client.generate_text.side_effect = Exception("Reflection failed")
        mock_client_class.return_value = mock_client
        
        agent = ReflectorAgent()
        context = {"draft": "Test draft"}
        
        with pytest.raises(Exception) as exc_info:
            agent.run_async(context)
        
        assert "Reflection failed" in str(exc_info.value)
    
    def test_get_description(self):
        """Test agent description."""
        agent = ReflectorAgent()
        description = agent.get_description()
        
        assert isinstance(description, str)
        assert "reflect" in description.lower()
        assert "critique" in description.lower()


class TestReviserAgentUnit:
    """Unit tests for ReviserAgent."""
    
    @patch('src.agents.reviser.LMStudioClient')
    def test_init(self, mock_client_class):
        """Test agent initialization."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReviserAgent("http://test:8080/v1")
        
        assert agent.client == mock_client
        mock_client_class.assert_called_once_with("http://test:8080/v1")
    
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
        mock_client.generate_text.assert_called_once()
    
    @patch('src.agents.reviser.LMStudioClient')
    def test_execute_missing_draft(self, mock_client_class):
        """Test execution with missing draft."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReviserAgent()
        context = {"critique": "Test critique"}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Both draft and critique are required for revision" in str(exc_info.value)
    
    @patch('src.agents.reviser.LMStudioClient')
    def test_execute_missing_critique(self, mock_client_class):
        """Test execution with missing critique."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        agent = ReviserAgent()
        context = {"draft": "Test draft"}
        
        with pytest.raises(ValueError) as exc_info:
            agent.run_async(context)
        
        assert "Both draft and critique are required for revision" in str(exc_info.value)
    
    @patch('src.agents.reviser.LMStudioClient')
    def test_execute_revision_error(self, mock_client_class):
        """Test execution with revision error."""
        mock_client = Mock()
        mock_client.generate_text.side_effect = Exception("Revision failed")
        mock_client_class.return_value = mock_client
        
        agent = ReviserAgent()
        context = {"draft": "Test draft", "critique": "Test critique"}
        
        with pytest.raises(Exception) as exc_info:
            agent.run_async(context)
        
        assert "Revision failed" in str(exc_info.value)
    
    def test_get_description(self):
        """Test agent description."""
        agent = ReviserAgent()
        description = agent.get_description()
        
        assert isinstance(description, str)
        assert "revise" in description.lower()
        assert "final" in description.lower()
