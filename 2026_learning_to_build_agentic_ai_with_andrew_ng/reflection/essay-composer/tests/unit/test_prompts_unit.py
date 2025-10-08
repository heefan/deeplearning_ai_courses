"""
Unit tests for prompt templates.
"""
import pytest
from prompts import EssayPrompts


class TestEssayPromptsUnit:
    """Unit tests for EssayPrompts."""
    
    def test_get_generator_prompt_basic(self):
        """Test basic generator prompt creation."""
        topic = "Artificial Intelligence"
        prompt = EssayPrompts.get_generator_prompt(topic)
        
        assert topic in prompt
        assert "well-structured essay" in prompt
        assert "introduction, body paragraphs, and conclusion" in prompt
        assert "500-800 words" in prompt
        assert "formal, academic tone" in prompt
    
    def test_get_generator_prompt_empty_topic(self):
        """Test generator prompt with empty topic."""
        topic = ""
        prompt = EssayPrompts.get_generator_prompt(topic)
        
        assert topic in prompt
        assert "well-structured essay" in prompt
    
    def test_get_generator_prompt_special_characters(self):
        """Test generator prompt with special characters in topic."""
        topic = "AI & Machine Learning: The Future?"
        prompt = EssayPrompts.get_generator_prompt(topic)
        
        assert topic in prompt
        assert "well-structured essay" in prompt
    
    def test_get_reflector_prompt_basic(self):
        """Test basic reflector prompt creation."""
        draft = "This is a sample essay draft about technology."
        prompt = EssayPrompts.get_reflector_prompt(draft)
        
        assert draft in prompt
        assert "critique" in prompt.lower()
        assert "Structure and Organization" in prompt
        assert "Argument Quality" in prompt
        assert "Clarity and Coherence" in prompt
        assert "Evidence and Examples" in prompt
        assert "Writing Quality" in prompt
        assert "Areas for Improvement" in prompt
    
    def test_get_reflector_prompt_long_draft(self):
        """Test reflector prompt with long draft."""
        draft = "A" * 1000  # Very long draft
        prompt = EssayPrompts.get_reflector_prompt(draft)
        
        assert draft in prompt
        assert "critique" in prompt.lower()
    
    def test_get_reflector_prompt_empty_draft(self):
        """Test reflector prompt with empty draft."""
        draft = ""
        prompt = EssayPrompts.get_reflector_prompt(draft)
        
        assert draft in prompt
        assert "critique" in prompt.lower()
    
    def test_get_revision_prompt_basic(self):
        """Test basic revision prompt creation."""
        draft = "Original essay content about AI."
        critique = "This essay needs improvement in structure and clarity."
        prompt = EssayPrompts.get_revision_prompt(draft, critique)
        
        assert draft in prompt
        assert critique in prompt
        assert "revise" in prompt.lower()
        assert "incorporating the feedback" in prompt
        assert "polished, final version" in prompt
    
    def test_get_revision_prompt_detailed_critique(self):
        """Test revision prompt with detailed critique."""
        draft = "Short essay."
        critique = "The essay lacks depth. Add more examples. Improve conclusion. Better transitions needed."
        prompt = EssayPrompts.get_revision_prompt(draft, critique)
        
        assert draft in prompt
        assert critique in prompt
        assert "revise" in prompt.lower()
    
    def test_prompt_structure_consistency(self):
        """Test that all prompts have consistent structure."""
        topic = "Test Topic"
        draft = "Test Draft"
        critique = "Test Critique"
        
        gen_prompt = EssayPrompts.get_generator_prompt(topic)
        ref_prompt = EssayPrompts.get_reflector_prompt(draft)
        rev_prompt = EssayPrompts.get_revision_prompt(draft, critique)
        
        # All prompts should be non-empty strings
        assert len(gen_prompt) > 0
        assert len(ref_prompt) > 0
        assert len(rev_prompt) > 0
        
        # Prompts should contain relevant keywords
        assert "essay" in gen_prompt.lower()
        assert "critique" in ref_prompt.lower()
        assert "revise" in rev_prompt.lower()
    
    def test_prompt_encoding_handling(self):
        """Test that prompts handle different encodings properly."""
        topic = "Café & Résumé: Special Characters"
        draft = "Essay with émojis 🚀 and special chars: café, naïve"
        critique = "Critique with special chars: résumé, naïve"
        
        gen_prompt = EssayPrompts.get_generator_prompt(topic)
        ref_prompt = EssayPrompts.get_reflector_prompt(draft)
        rev_prompt = EssayPrompts.get_revision_prompt(draft, critique)
        
        # Should handle special characters without errors
        assert isinstance(gen_prompt, str)
        assert isinstance(ref_prompt, str)
        assert isinstance(rev_prompt, str)
        
        # Should preserve special characters
        assert topic in gen_prompt
        assert draft in ref_prompt
        assert draft in rev_prompt
        assert critique in rev_prompt
