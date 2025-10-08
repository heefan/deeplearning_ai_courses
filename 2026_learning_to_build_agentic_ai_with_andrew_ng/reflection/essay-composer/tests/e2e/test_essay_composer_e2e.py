"""
End-to-end tests for the essay composer with ADK integration.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from essay_composer import EssayComposer


class TestEssayComposerE2E:
    """End-to-end tests for the complete essay composition workflow."""
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_adk_workflow_e2e_success(self, mock_orchestrator_class):
        """Test complete ADK workflow from start to finish."""
        # Setup orchestrator mock
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        # Mock successful workflow execution
        expected_result = {
            "topic": "The Future of AI",
            "draft": "AI will revolutionize the world...",
            "critique": "The essay needs more examples...",
            "final_essay": "Artificial Intelligence represents a paradigm shift...",
            "workflow_status": "completed"
        }
        mock_orchestrator.compose_essay.return_value = expected_result
        
        # Test the complete workflow
        composer = EssayComposer(use_adk=True)
        result = composer.compose_essay("The Future of AI", verbose=False)
        
        # Verify orchestrator was called correctly
        mock_orchestrator.compose_essay.assert_called_once_with("The Future of AI", False)
        
        # Verify complete result
        assert result["topic"] == "The Future of AI"
        assert result["draft"] == "AI will revolutionize the world..."
        assert result["critique"] == "The essay needs more examples..."
        assert result["final_essay"] == "Artificial Intelligence represents a paradigm shift..."
        assert result["workflow_status"] == "completed"
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_adk_workflow_e2e_verbose(self, mock_orchestrator_class):
        """Test complete ADK workflow with verbose output."""
        # Setup orchestrator mock
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        # Mock workflow execution with verbose output
        expected_result = {
            "topic": "Climate Change",
            "draft": "Climate change is a pressing issue...",
            "critique": "The essay could use more data...",
            "final_essay": "Climate change represents one of the greatest challenges...",
            "workflow_status": "completed"
        }
        mock_orchestrator.compose_essay.return_value = expected_result
        
        # Test with verbose output
        composer = EssayComposer(use_adk=True)
        result = composer.compose_essay("Climate Change", verbose=True)
        
        # Verify orchestrator was called with verbose=True
        mock_orchestrator.compose_essay.assert_called_once_with("Climate Change", True)
        assert result["workflow_status"] == "completed"
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_adk_workflow_e2e_error_handling(self, mock_orchestrator_class):
        """Test ADK workflow error handling."""
        # Setup orchestrator mock
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        # Mock workflow execution failure
        mock_orchestrator.compose_essay.side_effect = Exception("ADK workflow failed")
        
        composer = EssayComposer(use_adk=True)
        
        with pytest.raises(Exception) as exc_info:
            composer.compose_essay("Test Topic", verbose=False)
        
        assert "ADK workflow failed" in str(exc_info.value)
    
    @patch('essay_composer.LMStudioClient')
    @patch('essay_composer.prompts.EssayPrompts')
    def test_legacy_workflow_e2e_success(self, mock_prompts_class, mock_client_class):
        """Test complete legacy workflow from start to finish."""
        # Setup mocks
        mock_client = Mock()
        mock_prompts = Mock()
        mock_client_class.return_value = mock_client
        mock_prompts_class.return_value = mock_prompts
        
        # Mock successful generation steps
        mock_prompts.get_generator_prompt.return_value = "Generate essay about..."
        mock_prompts.get_reflector_prompt.return_value = "Critique this essay..."
        mock_prompts.get_revision_prompt.return_value = "Revise this essay..."
        
        mock_client.generate_text.side_effect = [
            "Generated draft essay",
            "Critique feedback",
            "Final revised essay"
        ]
        
        # Test legacy workflow
        composer = EssayComposer(use_adk=False)
        result = composer.compose_essay("Test Topic", verbose=False)
        
        # Verify all steps were called
        assert mock_prompts.get_generator_prompt.call_count == 1
        assert mock_prompts.get_reflector_prompt.call_count == 1
        assert mock_prompts.get_revision_prompt.call_count == 1
        assert mock_client.generate_text.call_count == 3
        
        # Verify result structure
        assert result["topic"] == "Test Topic"
        assert result["draft"] == "Generated draft essay"
        assert result["critique"] == "Critique feedback"
        assert result["final_essay"] == "Final revised essay"
    
    @patch('essay_composer.LMStudioClient')
    @patch('essay_composer.prompts.EssayPrompts')
    def test_legacy_workflow_e2e_error_handling(self, mock_prompts_class, mock_client_class):
        """Test legacy workflow error handling."""
        # Setup mocks
        mock_client = Mock()
        mock_prompts = Mock()
        mock_client_class.return_value = mock_client
        mock_prompts_class.return_value = mock_prompts
        
        # Mock generation failure
        mock_prompts.get_generator_prompt.return_value = "Generate essay about..."
        mock_client.generate_text.side_effect = Exception("Generation failed")
        
        composer = EssayComposer(use_adk=False)
        
        with pytest.raises(Exception) as exc_info:
            composer.compose_essay("Test Topic", verbose=False)
        
        assert "Generation failed" in str(exc_info.value)
    
    def test_composer_initialization_modes(self):
        """Test composer initialization in different modes."""
        # Test ADK mode
        with patch('essay_composer.EssayComposerOrchestrator') as mock_orchestrator:
            composer_adk = EssayComposer(use_adk=True)
            assert composer_adk.use_adk is True
            assert hasattr(composer_adk, 'orchestrator')
        
        # Test legacy mode
        with patch('essay_composer.LMStudioClient') as mock_client, \
             patch('essay_composer.EssayPrompts') as mock_prompts:
            composer_legacy = EssayComposer(use_adk=False)
            assert composer_legacy.use_adk is False
            assert hasattr(composer_legacy, 'client')
            assert hasattr(composer_legacy, 'prompts')
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_adk_workflow_with_different_topics(self, mock_orchestrator_class):
        """Test ADK workflow with various topic types."""
        # Setup orchestrator mock
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        # Test different topic types
        topics = [
            "Simple topic",
            "Complex topic with special characters: AI & ML",
            "Very long topic that might cause issues with prompt generation and processing",
            "Topic with numbers: 2024 AI Trends",
            "Topic with emojis: 🚀 Future of Technology 🤖"
        ]
        
        for topic in topics:
            expected_result = {
                "topic": topic,
                "draft": f"Draft for {topic}",
                "critique": f"Critique for {topic}",
                "final_essay": f"Final essay for {topic}",
                "workflow_status": "completed"
            }
            mock_orchestrator.compose_essay.return_value = expected_result
            
            composer = EssayComposer(use_adk=True)
            result = composer.compose_essay(topic, verbose=False)
            
            assert result["topic"] == topic
            assert result["workflow_status"] == "completed"
    
    @patch('essay_composer.EssayComposerOrchestrator')
    def test_adk_workflow_performance_simulation(self, mock_orchestrator_class):
        """Test ADK workflow performance characteristics."""
        # Setup orchestrator mock
        mock_orchestrator = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator
        
        # Simulate different performance scenarios
        performance_scenarios = [
            {"latency": 0.1, "success": True},
            {"latency": 1.0, "success": True},
            {"latency": 5.0, "success": True},
            {"latency": 0.1, "success": False}
        ]
        
        for scenario in performance_scenarios:
            if scenario["success"]:
                expected_result = {
                    "topic": "Performance Test",
                    "workflow_status": "completed"
                }
                mock_orchestrator.compose_essay.return_value = expected_result
                
                composer = EssayComposer(use_adk=True)
                result = composer.compose_essay("Performance Test", verbose=False)
                assert result["workflow_status"] == "completed"
            else:
                mock_orchestrator.compose_essay.side_effect = Exception("Performance failure")
                
                composer = EssayComposer(use_adk=True)
                with pytest.raises(Exception):
                    composer.compose_essay("Performance Test", verbose=False)
