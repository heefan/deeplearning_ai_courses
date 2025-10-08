"""
LM Studio API client for essay composer reflection pattern.
"""
import openai
from typing import Optional


class LMStudioClient:
    """Client for interacting with LM Studio API."""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio"):
        """Initialize the LM Studio client.
        
        Args:
            base_url: LM Studio API endpoint
            api_key: API key (can be any string for LM Studio)
        """
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key
        )
    
    def generate_text(self, prompt: str, model: str = "openai/gpt-oss-20b", max_tokens: int = 2000) -> str:
        """Generate text using the LM Studio model.
        
        Args:
            prompt: Input prompt for the model
            model: Model name (default: "local-model")
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test if LM Studio is running and accessible.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.generate_text("Hello", max_tokens=10)
            return True
        except:
            return False
