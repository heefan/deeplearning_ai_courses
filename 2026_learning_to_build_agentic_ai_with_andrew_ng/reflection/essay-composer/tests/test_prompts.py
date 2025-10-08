"""
Tests for prompt templates.
"""
import pytest
from prompts import EssayPrompts


class TestEssayPrompts:
    """Test cases for EssayPrompts."""
    
    def test_get_generator_prompt(self):
        """Test generator prompt creation."""
        topic = "Artificial Intelligence"
        prompt = EssayPrompts.get_generator_prompt(topic)
        
        assert topic in prompt
        assert "well-structured essay" in prompt
        assert "introduction, body paragraphs, and conclusion" in prompt
        assert "500-800 words" in prompt
    
    def test_get_reflector_prompt(self):
        """Test reflector prompt creation."""
        draft = "This is a sample essay draft."
        prompt = EssayPrompts.get_reflector_prompt(draft)
        
        assert draft in prompt
        assert "critique" in prompt.lower()
        assert "Structure and Organization" in prompt
        assert "Argument Quality" in prompt
        assert "Clarity and Coherence" in prompt
    
    def test_get_revision_prompt(self):
        """Test revision prompt creation."""
        draft = "Original essay content"
        critique = "This essay needs improvement in structure"
        prompt = EssayPrompts.get_revision_prompt(draft, critique)
        
        assert draft in prompt
        assert critique in prompt
        assert "revise" in prompt.lower()
        assert "incorporating the feedback" in prompt
        assert "polished, final version" in prompt
    
    def test_prompt_structure(self):
        """Test that prompts have proper structure."""
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
