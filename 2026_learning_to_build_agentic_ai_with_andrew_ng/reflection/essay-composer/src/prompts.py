"""
Prompt templates for the essay composer reflection pattern.
"""


class EssayPrompts:
    """Collection of prompts for essay generation, reflection, and revision."""
    
    @staticmethod
    def get_generator_prompt(topic: str) -> str:
        """Generate prompt for creating initial essay draft.
        
        Args:
            topic: Essay topic
            
        Returns:
            Formatted prompt for essay generation
        """
        return f"""Write a well-structured essay on: "{topic}"

Include: introduction, body paragraphs, and conclusion.
Aim for 500-800 words.
Use clear arguments and examples.
Write in a formal, academic tone.

Essay:"""

    @staticmethod
    def get_reflector_prompt(draft: str) -> str:
        """Generate prompt for critiquing the essay draft.
        
        Args:
            draft: The essay draft to critique
            
        Returns:
            Formatted prompt for reflection/critique
        """
        return f"""Critique this essay. Focus on:
- Structure and Organization
- Argument Quality
- Clarity and Coherence
- Evidence and Examples
- Writing Quality
- Areas for Improvement
- Specific improvement suggestions

Essay:
{draft}

Critique:"""

    @staticmethod
    def get_revision_prompt(draft: str, critique: str) -> str:
        """Generate prompt for revising the essay based on critique.
        
        Args:
            draft: Original essay draft
            critique: The critique/feedback
            
        Returns:
            Formatted prompt for essay revision
        """
        return f"""Revise this essay based on the feedback:

Original:
{draft}

Feedback:
{critique}

Write an improved version incorporating the feedback. Write a polished, final version:

Revised Essay:"""
