"""
Tests for the main essay composer functionality.
"""
import pytest
from unittest.mock import Mock, patch
from essay_composer import EssayComposer


class TestEssayComposer:
    """Test cases for EssayComposer."""
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_init(self, mock_orchestrator_class):
        """Test composer initialization."""
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        composer = EssayComposer("http://test:8080/v1")
        
        assert hasattr(composer, 'orchestrator')
        mock_orchestrator_class.assert_called_once_with("http://test:8080/v1")
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_compose_essay_success(self, mock_orchestrator_class):
        """Test successful essay composition."""
        # Mock the orchestrator and its methods
        mock_orchestrator = Mock()
        mock_orchestrator.compose_essay.return_value = {
            "topic": "Test Topic",
            "draft": "Draft essay content",
            "critique": "Critique feedback",
            "final_essay": "Final essay content",
            "workflow_status": "completed"
        }
        mock_orchestrator_class.return_value = mock_orchestrator
        
        composer = EssayComposer()
        result = composer.compose_essay("Test Topic", verbose=False)
        
        # Verify the result structure
        assert result["topic"] == "Test Topic"
        assert result["draft"] == "Draft essay content"
        assert result["critique"] == "Critique feedback"
        assert result["final_essay"] == "Final essay content"
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_compose_essay_error(self, mock_orchestrator_class):
        """Test essay composition with error."""
        # Mock orchestrator to raise an exception
        mock_orchestrator = Mock()
        mock_orchestrator.compose_essay.side_effect = Exception("Generation failed")
        mock_orchestrator_class.return_value = mock_orchestrator
        
        composer = EssayComposer()
        
        with pytest.raises(Exception) as exc_info:
            composer.compose_essay("Test Topic", verbose=False)
        
        assert "Generation failed" in str(exc_info.value)
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_compose_essay_verbose_output(self, mock_orchestrator_class, capsys):
        """Test that verbose mode shows intermediate steps."""
        # Mock the orchestrator to simulate verbose output
        def mock_compose_essay(topic, verbose):
            if verbose:
                print(f"🎯 Topic: {topic}")
                print("=" * 50)
                print("🤖 Starting ADK SequentialAgent Workflow...")
                print("=" * 50)
                print("\n📄 DRAFT ESSAY:")
                print("-" * 30)
                print("Draft content")
                print("\n" + "=" * 50)
                print("\n💭 CRITIQUE:")
                print("-" * 30)
                print("Critique content")
                print("\n" + "=" * 50)
                print("\n✨ FINAL ESSAY:")
                print("-" * 30)
                print("Final content")
                print(f"\n🎉 Essay completed successfully using ADK SequentialAgent!")
                print(f"Topic: {topic}")
                print(f"Workflow Status: completed")
            
            return {
                "topic": topic,
                "draft": "Draft content",
                "critique": "Critique content",
                "final_essay": "Final content",
                "workflow_status": "completed"
            }
        
        mock_orchestrator = Mock()
        mock_orchestrator.compose_essay.side_effect = mock_compose_essay
        mock_orchestrator_class.return_value = mock_orchestrator
        
        composer = EssayComposer()
        result = composer.compose_essay("Test Topic", verbose=True)
        
        # Capture the output
        captured = capsys.readouterr()
        
        # Verify verbose output contains expected elements
        assert "Test Topic" in captured.out
        assert "Draft content" in captured.out
        assert "Critique content" in captured.out
        assert "Final content" in captured.out
