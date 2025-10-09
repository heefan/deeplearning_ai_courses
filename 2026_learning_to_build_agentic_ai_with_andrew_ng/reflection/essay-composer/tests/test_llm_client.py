"""
Tests for LM Studio client functionality.
"""
import pytest
from src.lmstudio_client import LMStudioClient


class TestLMStudioClient:
    """Test cases for LMStudioClient."""
    
    def test_init_default_url(self):
        """Test client initialization with default URL."""
        client = LMStudioClient()
        assert str(client.client.base_url) == "http://localhost:1234/v1/"
    
    def test_init_custom_url(self):
        """Test client initialization with custom URL."""
        client = LMStudioClient("http://localhost:8080/v1")
        assert str(client.client.base_url) == "http://localhost:8080/v1/"
   
    def test_generate_text_success(self):
        """Test successful text generation with real LM Studio."""
        client = LMStudioClient("http://localhost:1234/v1")
        result = client.generate_text("Hello, how are you?")
        
        # Real assertions with real LM Studio
        assert result is not None
        assert len(result) > 0
        assert isinstance(result, str)
    
    def test_generate_text_error(self):
        """Test text generation with invalid URL."""
        client = LMStudioClient("http://localhost:9999/v1")  # Invalid port
        
        with pytest.raises(Exception):
            client.generate_text("Test prompt")
    
    def test_test_connection_success(self):
        """Test successful connection to LM Studio."""
        client = LMStudioClient("http://localhost:1234/v1")
        assert client.test_connection() is True
    
    def test_test_connection_failure(self):
        """Test failed connection to LM Studio."""
        client = LMStudioClient("http://localhost:9999/v1")  # Invalid port
        assert client.test_connection() is False
