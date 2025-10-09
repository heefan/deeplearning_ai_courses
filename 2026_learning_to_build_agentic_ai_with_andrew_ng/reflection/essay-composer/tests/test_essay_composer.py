"""
Tests for the main essay composer functionality.
"""
import pytest
from src.essay_composer import EssayComposer


class TestEssayComposer:
    """Test cases for EssayComposer."""
    
    def test_init(self):
        """Test composer initialization."""
        composer = EssayComposer("http://localhost:1234/v1")
        
        assert hasattr(composer, 'orchestrator')
        assert composer.orchestrator is not None
    
    def test_compose_essay_success(self):
        """Test successful essay composition."""
        composer = EssayComposer("http://localhost:1234/v1")
        result = composer.compose_essay("Test Topic", verbose=False)
        
        # Verify the result structure
        assert "topic" in result
        assert "draft" in result
        assert "critique" in result
        assert "final_essay" in result
        assert result["topic"] == "Test Topic"
    
    def test_compose_essay_error(self):
        """Test essay composition with error."""
        # Test with invalid URL to trigger error
        composer = EssayComposer("http://localhost:9999/v1")  # Invalid port
        
        with pytest.raises(Exception):
            composer.compose_essay("Test Topic", verbose=False)
    
    def test_compose_essay_verbose_output(self, capsys):
        """Test that verbose mode shows intermediate steps."""
        composer = EssayComposer("http://localhost:1234/v1")
        result = composer.compose_essay("Test Topic", verbose=True)
        
        # Capture the output
        captured = capsys.readouterr()
        
        # Verify verbose output contains expected elements
        assert "Test Topic" in captured.out
        assert "DRAFT ESSAY" in captured.out
        assert "CRITIQUE" in captured.out
        assert "FINAL ESSAY" in captured.out
