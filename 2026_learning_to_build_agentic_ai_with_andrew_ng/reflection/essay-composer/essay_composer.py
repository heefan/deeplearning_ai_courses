#!/usr/bin/env python3
"""
Essay Composer with Reflection Pattern using Google ADK

A CLI tool that uses the reflection AI design pattern with Google's Agent Development Kit
to generate high-quality essays. The process involves: Generation → Reflection → Revision
"""

import click
import sys
from agents.orchestrator import EssayComposerOrchestrator
from llm_client import LMStudioClient


class EssayComposer:
    """Main essay composer class using ADK agents."""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234/v1", use_adk: bool = True):
        """Initialize the essay composer.
        
        Args:
            lm_studio_url: LM Studio API endpoint
            use_adk: Whether to use ADK agents (default: True)
        """
        self.lm_studio_url = lm_studio_url
        self.use_adk = use_adk
        
        if use_adk:
            self.orchestrator = EssayComposerOrchestrator(lm_studio_url)
        else:
            # Fallback to original implementation
            from prompts import EssayPrompts
            self.client = LMStudioClient(lm_studio_url)
            self.prompts = EssayPrompts()
    
    def compose_essay(self, topic: str, verbose: bool = True) -> dict:
        """Compose an essay using the reflection pattern.
        
        Args:
            topic: Essay topic
            verbose: Whether to show intermediate steps
            
        Returns:
            Dictionary containing draft, critique, and final essay
        """
        if self.use_adk:
            return self._compose_with_adk(topic, verbose)
        else:
            return self._compose_legacy(topic, verbose)
    
    def _compose_with_adk(self, topic: str, verbose: bool = True) -> dict:
        """Compose essay using ADK agents."""
        return self.orchestrator.compose_essay(topic, verbose)
    
    def _compose_legacy(self, topic: str, verbose: bool = True) -> dict:
        """Legacy composition method (fallback)."""
        if verbose:
            click.echo(f"🎯 Topic: {topic}")
            click.echo("=" * 50)
            click.echo("📝 Using legacy composition method...")
        
        # Step 1: Generate initial draft
        if verbose:
            click.echo("📝 Generating initial draft...")
        
        draft_prompt = self.prompts.get_generator_prompt(topic)
        draft = self.client.generate_text(draft_prompt)
        
        if verbose:
            click.echo("\n📄 DRAFT ESSAY:")
            click.echo("-" * 30)
            click.echo(draft)
            click.echo("\n" + "=" * 50)
        
        # Step 2: Reflect and critique
        if verbose:
            click.echo("🔍 Reflecting on the draft...")
        
        critique_prompt = self.prompts.get_reflector_prompt(draft)
        critique = self.client.generate_text(critique_prompt)
        
        if verbose:
            click.echo("\n💭 CRITIQUE:")
            click.echo("-" * 30)
            click.echo(critique)
            click.echo("\n" + "=" * 50)
        
        # Step 3: Revise based on critique
        if verbose:
            click.echo("✏️  Revising essay based on feedback...")
        
        revision_prompt = self.prompts.get_revision_prompt(draft, critique)
        final_essay = self.client.generate_text(revision_prompt)
        
        if verbose:
            click.echo("\n✨ FINAL ESSAY:")
            click.echo("-" * 30)
        
        click.echo(final_essay)
        
        return {
            "topic": topic,
            "draft": draft,
            "critique": critique,
            "final_essay": final_essay
        }


@click.command()
@click.argument('topic', type=str)
@click.option('--url', default='http://localhost:1234/v1', 
              help='LM Studio API URL (default: http://localhost:1234/v1)')
@click.option('--quiet', '-q', is_flag=True, 
              help='Only show the final essay (no intermediate steps)')
@click.option('--test', is_flag=True, 
              help='Test connection to LM Studio')
@click.option('--legacy', is_flag=True, 
              help='Use legacy composition method (without ADK)')
@click.option('--workflow-info', is_flag=True, 
              help='Show ADK workflow information')
def main(topic: str, url: str, quiet: bool, test: bool, legacy: bool, workflow_info: bool):
    """Essay Composer - Generate high-quality essays using AI reflection with Google ADK.
    
    TOPIC: The essay topic to write about
    """
    composer = EssayComposer(url, use_adk=not legacy)
    
    # Show workflow info if requested
    if workflow_info:
        if composer.use_adk:
            info = composer.orchestrator.get_workflow_info()
            click.echo("🤖 ADK Workflow Information:")
            click.echo("=" * 40)
            for agent, description in info.items():
                click.echo(f"{agent}: {description}")
        else:
            click.echo("📝 Using legacy composition method (no ADK)")
        sys.exit(0)
    
    # Test connection if requested
    if test:
        click.echo("Testing connection to LM Studio...")
        if composer.use_adk:
            # Test with orchestrator's generator agent
            test_client = composer.orchestrator.generator.client
        else:
            test_client = composer.client
        
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
            if composer.use_adk:
                click.echo(f"Workflow Status: {result.get('workflow_status', '')}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        click.echo("Make sure LM Studio is running and accessible.", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
