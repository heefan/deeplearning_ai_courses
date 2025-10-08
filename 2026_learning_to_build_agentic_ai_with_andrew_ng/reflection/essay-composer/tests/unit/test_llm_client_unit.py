"""
Unit tests for LM Studio client functionality.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from llm_client import LMStudioClient


class TestLMStudioClientUnit:
    """Unit tests for LMStudioClient."""
    
    def test_init_default_params(self):
        """Test client initialization with default parameters."""
        with patch('llm_client.openai.OpenAI') as mock_openai:
            client = LMStudioClient()
            mock_openai.assert_called_once_with(
                base_url="http://localhost:1234/v1",
                api_key="lm-studio"
            )
    
    def test_init_custom_params(self):
        """Test client initialization with custom parameters."""
        with patch('llm_client.openai.OpenAI') as mock_openai:
            client = LMStudioClient("http://custom:8080/v1", "custom-key")
            mock_openai.assert_called_once_with(
                base_url="http://custom:8080/v1",
                api_key="custom-key"
            )
    
    def test_generate_text_success(self):
        """Test successful text generation."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Generated text response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            result = client.generate_text("Test prompt")
            
            assert result == "Generated text response"
            mock_client.chat.completions.create.assert_called_once_with(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": "Test prompt"}],
                max_tokens=2000,
                temperature=0.7
            )
    
    def test_generate_text_custom_params(self):
        """Test text generation with custom parameters."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Custom response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            result = client.generate_text("Test prompt", model="custom-model", max_tokens=1000)
            
            assert result == "Custom response"
            mock_client.chat.completions.create.assert_called_once_with(
                model="custom-model",
                messages=[{"role": "user", "content": "Test prompt"}],
                max_tokens=1000,
                temperature=0.7
            )
    
    def test_generate_text_api_error(self):
        """Test text generation with API error."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("API Error")
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            
            with pytest.raises(Exception) as exc_info:
                client.generate_text("Test prompt")
            
            assert "Error generating text: API Error" in str(exc_info.value)
    
    def test_generate_text_network_error(self):
        """Test text generation with network error."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = ConnectionError("Network error")
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            
            with pytest.raises(Exception) as exc_info:
                client.generate_text("Test prompt")
            
            assert "Error generating text: Network error" in str(exc_info.value)
    
    def test_test_connection_success(self):
        """Test successful connection test."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Hello"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            assert client.test_connection() is True
    
    def test_test_connection_failure(self):
        """Test failed connection test."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = Exception("Connection failed")
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            assert client.test_connection() is False
    
    def test_test_connection_timeout(self):
        """Test connection test with timeout."""
        with patch('llm_client.openai.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = TimeoutError("Request timeout")
            mock_openai_class.return_value = mock_client
            
            client = LMStudioClient()
            assert client.test_connection() is False
