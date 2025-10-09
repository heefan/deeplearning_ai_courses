"""
Tests for the main essay composer functionality.
"""
import pytest
from unittest.mock import Mock, patch
from src.essay_composer import EssayComposer


class TestEssayComposer:
    """Test cases for EssayComposer."""
    
    def test_init(self):
        """Test composer initialization."""
        composer = EssayComposer("http://localhost:1234/v1")
        
        assert hasattr(composer, 'orchestrator')
        assert composer.orchestrator is not None
    
    @patch('src.essay_composer.EssayComposerOrchestrator')
    def test_compose_essay_success(self, mock_orchestrator_class):
        """Test successful essay composition."""
        # Setup mock orchestrator
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_orchestrator.compose_essay.return_value = {
            "topic": "Test Topic",
            "draft": "This is a test essay draft.",
            "critique": "This is a test critique.",
            "final_essay": "This is the final essay.",
            "workflow_status": "completed"
        }
        
        composer = EssayComposer("http://localhost:1234/v1")
        result = composer.compose_essay("Test Topic", verbose=False)
        
        # Verify the result structure
        assert "topic" in result
        assert "draft" in result
        assert "critique" in result
        assert "final_essay" in result
        assert result["topic"] == "Test Topic"
        
        # Verify orchestrator was called correctly
        mock_orchestrator.compose_essay.assert_called_once_with("Test Topic", False)
    
    @patch('src.essay_composer.EssayComposerOrchestrator')
    def test_compose_essay_error(self, mock_orchestrator_class):
        """Test essay composition with error."""
        # Setup mock orchestrator to raise an exception
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        mock_orchestrator.compose_essay.side_effect = Exception("Test error")
        
        composer = EssayComposer("http://localhost:1234/v1")
        
        with pytest.raises(Exception, match="Test error"):
            composer.compose_essay("Test Topic", verbose=False)
    
    @patch('src.essay_composer.EssayComposerOrchestrator')
    def test_compose_essay_verbose_output(self, mock_orchestrator_class, capsys):
        """Test that verbose mode shows intermediate steps."""
        # Setup mock orchestrator that simulates verbose output
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        def mock_compose_essay(topic, verbose):
            if verbose:
                print(f"🎯 Topic: {topic}")
                print("=" * 50)
                print("🤖 Starting ADK SequentialAgent Workflow...")
                print("=" * 50)
                print("\n📄 DRAFT ESSAY:")
                print("-" * 30)
                print("This is a test essay draft.")
                print("\n" + "=" * 50)
                print("\n💭 CRITIQUE:")
                print("-" * 30)
                print("This is a test critique.")
                print("\n" + "=" * 50)
                print("\n✨ FINAL ESSAY:")
                print("-" * 30)
                print("This is the final essay.")
                print(f"\n🎉 Essay completed successfully using ADK SequentialAgent!")
                print(f"Topic: {topic}")
                print(f"Workflow Status: completed")
            
            return {
                "topic": topic,
                "draft": "This is a test essay draft.",
                "critique": "This is a test critique.",
                "final_essay": "This is the final essay.",
                "workflow_status": "completed"
            }
        
        mock_orchestrator.compose_essay.side_effect = mock_compose_essay
        
        composer = EssayComposer("http://localhost:1234/v1")
        result = composer.compose_essay("Test Topic", verbose=True)
        
        # Capture the output
        captured = capsys.readouterr()
        
        # Verify verbose output contains expected elements
        assert "Test Topic" in captured.out
        assert "DRAFT ESSAY" in captured.out
        assert "CRITIQUE" in captured.out
        assert "FINAL ESSAY" in captured.out
