"""
End-to-end tests for CLI functionality.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from src.essay_composer import main


class TestCLIE2E:
    """End-to-end tests for CLI functionality."""
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_basic_usage_adk(self, mock_composer_class):
        """Test basic CLI usage with ADK mode."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.compose_essay.return_value = {
            "topic": "Test Topic",
            "final_essay": "Generated essay content"
        }
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic"])
        
        # Verify successful execution
        assert result.exit_code == 0
        assert "Test Topic" in result.output
        assert "Generated essay content" in result.output
        
        # Verify composer was initialized
        mock_composer_class.assert_called_once()
    
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_quiet_mode(self, mock_composer_class):
        """Test CLI usage with quiet mode."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.compose_essay.return_value = {
            "topic": "Test Topic",
            "final_essay": "Generated essay content"
        }
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic", "--quiet"])
        
        # Verify successful execution
        assert result.exit_code == 0
        assert "Generated essay content" in result.output
        
        # Verify compose_essay was called with verbose=False
        mock_composer.compose_essay.assert_called_once_with("Test Topic", verbose=False)
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_verbose_mode(self, mock_composer_class):
        """Test CLI usage with verbose mode (default)."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.compose_essay.return_value = {
            "topic": "Test Topic",
            "final_essay": "Generated essay content"
        }
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic"])
        
        # Verify successful execution
        assert result.exit_code == 0
        
        # Verify compose_essay was called with verbose=True (default)
        mock_composer.compose_essay.assert_called_once_with("Test Topic", verbose=True)
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_test_connection_success(self, mock_composer_class):
        """Test CLI test connection success."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.orchestrator.generator.client.test_connection.return_value = True
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic", "--test"])
        
        # Verify successful test
        assert result.exit_code == 0
        assert "Testing connection to LM Studio..." in result.output
        assert "✅ Connection successful!" in result.output
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_test_connection_failure(self, mock_composer_class):
        """Test CLI test connection failure."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.orchestrator.generator.client.test_connection.return_value = False
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic", "--test"])
        
        # Verify failed test
        assert result.exit_code == 1
        assert "Testing connection to LM Studio..." in result.output
        assert "❌ Connection failed!" in result.output
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_workflow_info_adk(self, mock_composer_class):
        """Test CLI workflow info with ADK mode."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.orchestrator.get_workflow_info.return_value = {
            "generator": "Generates essays",
            "reflector": "Critiques essays",
            "reviser": "Revises essays",
            "workflow_type": "Sequential ADK Workflow"
        }
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic", "--workflow-info"])
        
        # Verify workflow info display
        assert result.exit_code == 0
        assert "🤖 ADK Workflow Information:" in result.output
        assert "Generates essays" in result.output
        assert "Critiques essays" in result.output
        assert "Revises essays" in result.output
    
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_custom_url(self, mock_composer_class):
        """Test CLI with custom LM Studio URL."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.compose_essay.return_value = {
            "topic": "Test Topic",
            "final_essay": "Generated essay content"
        }
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic", "--url", "http://custom:8080/v1"])
        
        # Verify successful execution
        assert result.exit_code == 0
        
        # Verify composer was initialized with custom URL
        mock_composer_class.assert_called_once()
        call_args = mock_composer_class.call_args
        assert call_args[0][0] == "http://custom:8080/v1"
    
    @patch('src.essay_composer.EssayComposer')
    def test_cli_error_handling(self, mock_composer_class):
        """Test CLI error handling."""
        # Setup mocks
        mock_composer = Mock()
        mock_composer_class.return_value = mock_composer
        mock_composer.compose_essay.side_effect = Exception("Test error")
        
        runner = CliRunner()
        result = runner.invoke(main, ["Test Topic"])
        
        # Verify error handling
        assert result.exit_code == 1
        assert "❌ Error: Test error" in result.output
        assert "Make sure LM Studio is running and accessible." in result.output
    
    def test_cli_help(self):
        """Test CLI help output."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        
        # Verify help output
        assert result.exit_code == 0
        assert "Essay Composer - Generate high-quality essays" in result.output
        assert "TOPIC" in result.output
        assert "--url" in result.output
        assert "--quiet" in result.output
        assert "--test" in result.output
        assert "--workflow-info" in result.output
    
    def test_cli_missing_topic(self):
        """Test CLI with missing topic argument."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        
        # Verify error for missing topic
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output
