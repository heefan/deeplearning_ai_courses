"""
Unit tests for the CLI interface.

These tests verify the command-line interface functionality using
mocked dependencies to ensure fast and reliable testing.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from click.testing import CliRunner
from pathlib import Path

from src.cli.main import cli, _analyze_dataset, _show_config, _show_examples


class TestCLI:
    """Test cases for the CLI interface."""
    
    @pytest.fixture
    def runner(self):
        """Click test runner."""
        return CliRunner()
    
    @pytest.fixture
    def mock_csv_file(self, tmp_path):
        """Create a mock CSV file for testing."""
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text("date,coffee_name,price\n2024-01-01,Latte,3.50\n2024-01-02,Cappuccino,4.20")
        return csv_file
    
    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Chart Generation Agent" in result.output
        assert "generate" in result.output
        assert "analyze" in result.output
    
    def test_cli_version(self, runner):
        """Test CLI version command."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
    
    def test_generate_help(self, runner):
        """Test generate command help."""
        result = runner.invoke(cli, ["generate", "--help"])
        assert result.exit_code == 0
        assert "Generate a chart based on your query" in result.output
        assert "--csv-file" in result.output
        assert "--output-dir" in result.output
    
    def test_analyze_help(self, runner):
        """Test analyze command help."""
        result = runner.invoke(cli, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "Analyze the CSV file" in result.output
    
    def test_config_info_help(self, runner):
        """Test config-info command help."""
        result = runner.invoke(cli, ["config-info", "--help"])
        assert result.exit_code == 0
        assert "Show current configuration" in result.output
    
    def test_examples_help(self, runner):
        """Test examples command help."""
        result = runner.invoke(cli, ["examples", "--help"])
        assert result.exit_code == 0
        assert "Show example queries" in result.output
    
    def test_verbose_flag(self, runner):
        """Test verbose flag functionality."""
        result = runner.invoke(cli, ["--verbose", "--help"])
        assert result.exit_code == 0
        assert "Enable verbose output" in result.output
    
    @patch('src.cli.main._generate_chart')
    def test_generate_command_basic(self, mock_generate, runner, mock_csv_file):
        """Test basic generate command."""
        mock_generate.return_value = None
        
        result = runner.invoke(cli, [
            "generate",
            "Create a test chart",
            "--csv-file", str(mock_csv_file)
        ])
        
        assert result.exit_code == 0
        mock_generate.assert_called_once()
    
    @patch('src.cli.main._generate_chart')
    def test_generate_command_with_options(self, mock_generate, runner, mock_csv_file):
        """Test generate command with all options."""
        mock_generate.return_value = None
        
        result = runner.invoke(cli, [
            "--verbose",
            "generate",
            "Create a test chart",
            "--csv-file", str(mock_csv_file),
            "--output-dir", "./test_output",
            "--max-iterations", "5",
            "--no-execute",
            "--timeout", "60"
        ])
        
        assert result.exit_code == 0
        mock_generate.assert_called_once()
    
    @patch('src.cli.main.DataSchema')
    def test_analyze_command(self, mock_data_schema, runner, mock_csv_file):
        """Test analyze command."""
        # Mock DataSchema
        mock_schema = Mock()
        mock_schema.df.shape = (100, 3)
        mock_schema.columns = ["date", "coffee_name", "price"]
        mock_schema.get_date_range.return_value = {"start": "2024-01-01", "end": "2024-12-31"}
        mock_schema.get_coffee_types.return_value = ["Latte", "Cappuccino", "Espresso"]
        mock_schema.get_sample_data.return_value = "Sample data here"
        mock_data_schema.return_value = mock_schema
        
        result = runner.invoke(cli, ["analyze", str(mock_csv_file)])
        
        assert result.exit_code == 0
        assert "Dataset Analysis" in result.output
        assert "100 rows, 3 columns" in result.output
    
    @patch('src.cli.main.config')
    def test_config_info_command(self, mock_config, runner):
        """Test config-info command."""
        # Mock config
        mock_config.lmstudio.base_url = "http://localhost:1234/v1"
        mock_config.lmstudio.model = "gpt-oss-20b"
        mock_config.app.max_reflection_iterations = 3
        mock_config.app.code_execution_timeout = 30
        mock_config.app.chart_output_dir = "./outputs"
        mock_config.app.debug = False
        mock_config.app.log_level = "INFO"
        
        result = runner.invoke(cli, ["config-info"])
        
        assert result.exit_code == 0
        assert "Configuration Settings" in result.output
        assert "http://localhost:1234/v1" in result.output
        assert "gpt-oss-20b" in result.output
    
    def test_examples_command(self, runner):
        """Test examples command."""
        result = runner.invoke(cli, ["examples"])
        
        assert result.exit_code == 0
        assert "Example Queries:" in result.output
        assert "chart-gen generate" in result.output
    
    def test_generate_missing_csv(self, runner):
        """Test generate command with non-existent CSV file."""
        result = runner.invoke(cli, [
            "generate",
            "Create a test chart",
            "--csv-file", "non_existent.csv"
        ])
        
        assert result.exit_code != 0
        assert "Error" in result.output
    
    def test_analyze_missing_csv(self, runner):
        """Test analyze command with non-existent CSV file."""
        result = runner.invoke(cli, ["analyze", "non_existent.csv"])
        
        assert result.exit_code != 0
        assert "Error" in result.output
    
    @patch('src.cli.main._generate_chart')
    def test_generate_with_verbose(self, mock_generate, runner, mock_csv_file):
        """Test generate command with verbose output."""
        mock_generate.return_value = None
        
        result = runner.invoke(cli, [
            "--verbose",
            "generate",
            "Create a test chart",
            "--csv-file", str(mock_csv_file)
        ])
        
        assert result.exit_code == 0
        assert "Verbose mode enabled" in result.output
    
    def test_analyze_dataset_success(self, mock_csv_file):
        """Test _analyze_dataset function directly."""
        with patch('src.cli.main.DataSchema') as mock_schema_class:
            mock_schema = Mock()
            mock_schema.df.shape = (50, 4)
            mock_schema.columns = ["date", "time", "coffee_name", "price"]
            mock_schema.get_date_range.return_value = {"start": "2024-01-01", "end": "2024-06-30"}
            mock_schema.get_coffee_types.return_value = ["Latte", "Cappuccino"]
            mock_schema.get_sample_data.return_value = "date,time,coffee_name,price\n2024-01-01,08:00,Latte,3.50"
            mock_schema_class.return_value = mock_schema
            
            # Should not raise exception
            _analyze_dataset(mock_csv_file)
    
    def test_analyze_dataset_error(self, tmp_path):
        """Test _analyze_dataset function with error."""
        fake_csv = tmp_path / "fake.csv"
        fake_csv.write_text("invalid,csv,data")
        
        with patch('src.cli.main.DataSchema') as mock_schema_class:
            mock_schema_class.side_effect = Exception("CSV parsing error")
            
            with pytest.raises(SystemExit):
                _analyze_dataset(fake_csv)
    
    def test_show_config(self):
        """Test _show_config function."""
        with patch('src.cli.main.config') as mock_config:
            mock_config.lmstudio.base_url = "http://test:1234/v1"
            mock_config.lmstudio.model = "test-model"
            mock_config.app.max_reflection_iterations = 5
            mock_config.app.code_execution_timeout = 60
            mock_config.app.chart_output_dir = "./test_output"
            mock_config.app.debug = True
            mock_config.app.log_level = "DEBUG"
            
            # Should not raise exception
            _show_config()
    
    def test_show_examples(self):
        """Test _show_examples function."""
        # Should not raise exception
        _show_examples()
    
    @patch('src.cli.main._generate_chart')
    def test_generate_chart_integration(
        self,
        mock_generate_chart,
        runner,
        mock_csv_file
    ):
        """Test generate command integration with mocked components."""
        # Mock the async function
        mock_generate_chart.return_value = None
        
        result = runner.invoke(cli, [
            "generate",
            "Create a test chart",
            "--csv-file", str(mock_csv_file)
        ])
        
        assert result.exit_code == 0
        mock_generate_chart.assert_called_once()
    
    def test_cli_with_config_file(self, runner, tmp_path):
        """Test CLI with config file option."""
        config_file = tmp_path / "config.env"
        config_file.write_text("LMSTUDIO_BASE_URL=http://test:1234/v1\nLMSTUDIO_MODEL=test-model")
        
        result = runner.invoke(cli, [
            "--config-file", str(config_file),
            "--help"
        ])
        
        assert result.exit_code == 0
    
    def test_generate_default_csv(self, runner):
        """Test generate command with default CSV file."""
        with patch('src.cli.main._generate_chart') as mock_generate:
            mock_generate.return_value = None
            
            # Mock that coffee_sales.csv exists
            with patch('pathlib.Path.exists', return_value=True):
                result = runner.invoke(cli, [
                    "generate",
                    "Create a test chart"
                ])
                
                assert result.exit_code == 0
                mock_generate.assert_called_once()
    
    def test_generate_no_execute_flag(self, runner, mock_csv_file):
        """Test generate command with --no-execute flag."""
        with patch('src.cli.main._generate_chart') as mock_generate:
            mock_generate.return_value = None
            
            result = runner.invoke(cli, [
                "generate",
                "Create a test chart",
                "--csv-file", str(mock_csv_file),
                "--no-execute"
            ])
            
            assert result.exit_code == 0
            # Verify that execute=False was passed
            call_args = mock_generate.call_args
            assert call_args[1]['execute'] is False
