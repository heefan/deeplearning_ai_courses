"""
Tests for LM Studio client functionality.
"""
import pytest
from unittest.mock import Mock, patch
from llm_client import LMStudioClient


class TestLMStudioClient:
    """Test cases for LMStudioClient."""
    
    def test_init_default_params(self):
        """Test client initialization with default parameters."""
        client = LMStudioClient()
        assert str(client.client.base_url) == "http://localhost:1234/v1/"
        assert client.client.api_key == "lm-studio"
    
    def test_init_custom_params(self):
        """Test client initialization with custom parameters."""
        client = LMStudioClient("http://custom:8080/v1", "custom-key")
        assert str(client.client.base_url) == "http://custom:8080/v1/"
        assert client.client.api_key == "custom-key"
    
    @patch('llm_client.openai.OpenAI')
    def test_generate_text_success(self, mock_openai):
        """Test successful text generation."""
        # Mock the OpenAI client and response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated text response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        client = LMStudioClient()
        result = client.generate_text("Test prompt")
        
        assert result == "Generated text response"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('llm_client.openai.OpenAI')
    def test_generate_text_error(self, mock_openai):
        """Test text generation with error."""
        # Mock the OpenAI client to raise an exception
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        client = LMStudioClient()
        
        with pytest.raises(Exception) as exc_info:
            client.generate_text("Test prompt")
        
        assert "Error generating text: API Error" in str(exc_info.value)
    
    @patch('llm_client.openai.OpenAI')
    def test_test_connection_success(self, mock_openai):
        """Test successful connection test."""
        # Mock successful connection
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hello"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        client = LMStudioClient()
        assert client.test_connection() is True
    
    @patch('llm_client.openai.OpenAI')
    def test_test_connection_failure(self, mock_openai):
        """Test failed connection test."""
        # Mock failed connection
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Connection failed")
        mock_openai.return_value = mock_client
        
        client = LMStudioClient()
        assert client.test_connection() is False
