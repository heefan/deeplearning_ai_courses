#!/usr/bin/env python3
"""
Essay Composer with Reflection Pattern using Google ADK

A CLI tool that uses the reflection AI design pattern with Google's Agent Development Kit
to generate high-quality essays. The process involves: Generation → Reflection → Revision
"""

import click
import sys
from src.agents.orchestrator import EssayComposerOrchestrator


class EssayComposer:
    """Essay composer using Google ADK agents."""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234/v1"):
        """Initialize the essay composer.
        
        Args:
            lm_studio_url: LM Studio API endpoint
        """
        self.lm_studio_url = lm_studio_url
        self.orchestrator = EssayComposerOrchestrator(lm_studio_url)
    
    def compose_essay(self, topic: str, verbose: bool = True) -> dict:
        """Compose an essay using ADK agents.
        
        Args:
            topic: Essay topic
            verbose: Whether to show intermediate steps
            
        Returns:
            Dictionary containing draft, critique, and final essay
        """
        return self.orchestrator.compose_essay(topic, verbose)
    


@click.command()
@click.argument('topic', type=str)
@click.option('--url', default='http://localhost:1234/v1', 
              help='LM Studio API URL (default: http://localhost:1234/v1)')
@click.option('--quiet', '-q', is_flag=True, 
              help='Only show the final essay (no intermediate steps)')
@click.option('--test', is_flag=True, 
              help='Test connection to LM Studio')
@click.option('--workflow-info', is_flag=True, 
              help='Show ADK workflow information')
@click.option('--legacy', is_flag=True, 
              help='Use legacy mode (deprecated)')
def main(topic: str, url: str, quiet: bool, test: bool, workflow_info: bool, legacy: bool):
    """Essay Composer - Generate high-quality essays using AI reflection with Google ADK.
    
    TOPIC: The essay topic to write about
    """
    composer = EssayComposer(url)
    
    # Handle legacy mode
    if legacy:
        click.echo("⚠️  Legacy mode is deprecated. Please use the standard ADK workflow.")
        # For now, just continue with normal workflow
        pass
    
    # Show workflow info if requested
    if workflow_info:
        info = composer.orchestrator.get_workflow_info()
        click.echo("🤖 ADK Workflow Information:")
        click.echo("=" * 40)
        for agent, description in info.items():
            click.echo(f"{agent}: {description}")
        sys.exit(0)
    
    # Test connection if requested
    if test:
        click.echo("Testing connection to LM Studio...")
        # Test with orchestrator's generator agent
        test_client = composer.orchestrator.generator.client
        
        if test_client.test_connection():
            click.echo("✅ Connection successful!")
            sys.exit(0)
        else:
            click.echo("❌ Connection failed! Make sure LM Studio is running.")
            sys.exit(1)
    
    try:
        # Compose the essay
        result = composer.compose_essay(topic, verbose=not quiet)
        
        if not quiet:
            click.echo(f"\n🎉 Essay completed successfully!")
            click.echo(f"Topic: {result['topic']}")
            click.echo(f"Workflow Status: {result.get('workflow_status', '')}")
        
        # Always print the final essay content (even in quiet mode)
        if 'final_essay' in result:
            click.echo(f"\nFinal Essay:\n{result['final_essay']}")
        elif 'draft' in result:
            click.echo(f"\nEssay:\n{result['draft']}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        click.echo("Make sure LM Studio is running and accessible.", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
