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
        return f"""Write a well-structured essay on the topic: "{topic}"

Requirements:
- Write a complete essay with introduction, body paragraphs, and conclusion
- Aim for 500-800 words
- Use clear, coherent arguments
- Include specific examples or evidence where appropriate
- Write in a formal, academic tone

Essay:"""

    @staticmethod
    def get_reflector_prompt(draft: str) -> str:
        """Generate prompt for critiquing the essay draft.
        
        Args:
            draft: The essay draft to critique
            
        Returns:
            Formatted prompt for reflection/critique
        """
        return f"""Please provide a detailed critique of the following essay. Focus on:

1. **Structure and Organization**: Is the essay well-organized with clear introduction, body, and conclusion?
2. **Argument Quality**: Are the arguments logical, well-supported, and persuasive?
3. **Clarity and Coherence**: Is the writing clear and easy to follow?
4. **Evidence and Examples**: Are claims supported with appropriate evidence?
5. **Writing Quality**: Grammar, style, and flow
6. **Areas for Improvement**: Specific suggestions for enhancement

Essay to critique:
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
        return f"""Based on the following essay draft and critique, write an improved version of the essay.

Original Essay:
{draft}

Critique and Feedback:
{critique}

Please revise the essay incorporating the feedback. Maintain the same topic and core arguments while addressing the identified issues. Write a polished, final version that is well-structured, clear, and persuasive.

Revised Essay:"""
