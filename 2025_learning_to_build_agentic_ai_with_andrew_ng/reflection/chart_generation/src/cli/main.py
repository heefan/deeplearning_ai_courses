"""
Main CLI interface for the chart generation agent.

This module provides the command-line interface using Click for easy interaction
with the reflection-based chart generation system.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ..agents.orchestrator import ReflectionOrchestrator
from ..agents.generator import GeneratorAgent
from ..agents.critic import CriticAgent
from ..executor.code_executor import CodeExecutor
from ..utils.data_schema import DataSchema
from ..config import config

# Initialize Rich console for beautiful CLI output
console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="chart-gen")
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.option(
    "--config-file", "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config_file: Optional[Path]) -> None:
    """
    Chart Generation Agent with Reflection Pattern
    
    A CLI tool for generating Python matplotlib code to visualize coffee sales data
    using the reflection AI design pattern.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config_file"] = config_file
    
    if verbose:
        console.print("[bold blue]Chart Generation Agent[/bold blue] - Verbose mode enabled")


@cli.command()
@click.argument("query", type=str)
@click.option(
    "--csv-file", "-f",
    type=click.Path(exists=True, path_type=Path),
    default="coffee_sales.csv",
    help="Path to CSV file (default: coffee_sales.csv)"
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(path_type=Path),
    default="./outputs",
    help="Output directory for generated charts (default: ./outputs)"
)
@click.option(
    "--max-iterations", "-i",
    type=int,
    default=3,
    help="Maximum reflection iterations (default: 3)"
)
@click.option(
    "--execute/--no-execute",
    default=True,
    help="Execute generated code to create charts (default: True)"
)
@click.option(
    "--timeout", "-t",
    type=int,
    default=30,
    help="Code execution timeout in seconds (default: 30)"
)
@click.pass_context
def generate(
    ctx: click.Context,
    query: str,
    csv_file: Path,
    output_dir: Path,
    max_iterations: int,
    execute: bool,
    timeout: int
) -> None:
    """
    Generate a chart based on your query.
    
    QUERY: Your request for chart generation (e.g., "Create a plot comparing Q1 coffee sales in 2024 and 2025")
    """
    asyncio.run(_generate_chart(
        query=query,
        csv_file=csv_file,
        output_dir=output_dir,
        max_iterations=max_iterations,
        execute=execute,
        timeout=timeout,
        verbose=ctx.obj["verbose"]
    ))


@cli.command()
@click.argument("csv_file", type=click.Path(exists=True, path_type=Path))
def analyze(csv_file: Path) -> None:
    """
    Analyze the CSV file and show dataset information.
    
    CSV_FILE: Path to the CSV file to analyze
    """
    _analyze_dataset(csv_file)


@cli.command()
def config_info() -> None:
    """Show current configuration settings."""
    _show_config()


@cli.command()
def examples() -> None:
    """Show example queries for chart generation."""
    _show_examples()


async def _generate_chart(
    query: str,
    csv_file: Path,
    output_dir: Path,
    max_iterations: int,
    execute: bool,
    timeout: int,
    verbose: bool
) -> None:
    """Generate chart based on query."""
    try:
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        console.print(f"[bold blue]Initializing Chart Generation Agent...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Initialize data schema
            task1 = progress.add_task("Loading dataset...", total=None)
            data_schema = DataSchema(str(csv_file))
            progress.update(task1, description="Dataset loaded successfully")
            
            # Initialize agents
            task2 = progress.add_task("Initializing agents...", total=None)
            model_config = config.get_model_config()
            generator = GeneratorAgent(model_config, data_schema)
            critic = CriticAgent(model_config)
            executor = CodeExecutor(timeout=timeout, output_dir=str(output_dir))
            orchestrator = ReflectionOrchestrator(generator, critic, executor, max_iterations)
            progress.update(task2, description="Agents initialized")
            
            # Generate chart
            task3 = progress.add_task("Generating chart...", total=None)
            result = await orchestrator.reflect_and_generate(query, execute_code=execute)
            progress.update(task3, description="Chart generation completed")
        
        # Display results
        _display_results(result, verbose)
        
        # Cleanup
        await orchestrator.close()
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        if verbose:
            console.print_exception()
        sys.exit(1)


def _analyze_dataset(csv_file: Path) -> None:
    """Analyze and display dataset information."""
    try:
        console.print(f"[bold blue]Analyzing dataset:[/bold blue] {csv_file}")
        
        data_schema = DataSchema(str(csv_file))
        
        # Create info table
        table = Table(title="Dataset Analysis")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("File", str(csv_file))
        table.add_row("Shape", f"{data_schema.df.shape[0]} rows, {data_schema.df.shape[1]} columns")
        table.add_row("Columns", ", ".join(data_schema.columns))
        
        # Date range
        date_range = data_schema.get_date_range()
        if date_range:
            table.add_row("Date Range", f"{date_range['start']} to {date_range['end']}")
        
        # Coffee types
        coffee_types = data_schema.get_coffee_types()
        if coffee_types:
            table.add_row("Coffee Types", f"{len(coffee_types)} types")
            table.add_row("", ", ".join(coffee_types[:5]) + ("..." if len(coffee_types) > 5 else ""))
        
        console.print(table)
        
        # Show sample data
        console.print("\n[bold blue]Sample Data:[/bold blue]")
        sample_data = data_schema.get_sample_data(3)
        console.print(Panel(sample_data, title="First 3 rows"))
        
    except Exception as e:
        console.print(f"[bold red]Error analyzing dataset:[/bold red] {str(e)}")
        sys.exit(1)


def _show_config() -> None:
    """Show current configuration."""
    table = Table(title="Configuration Settings")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("LMStudio URL", config.lmstudio.base_url)
    table.add_row("Model", config.lmstudio.model)
    table.add_row("Max Iterations", str(config.app.max_reflection_iterations))
    table.add_row("Execution Timeout", f"{config.app.code_execution_timeout}s")
    table.add_row("Output Directory", config.app.chart_output_dir)
    table.add_row("Debug Mode", str(config.app.debug))
    table.add_row("Log Level", config.app.log_level)
    
    console.print(table)


def _show_examples() -> None:
    """Show example queries."""
    examples = [
        "Create a plot comparing Q1 coffee sales in 2024 and 2025",
        "Create a bar chart showing sales by coffee type for 2024",
        "Create a line chart showing daily sales trends over time",
        "Create a pie chart showing the distribution of coffee types",
        "Create a comprehensive dashboard with multiple charts showing coffee sales analysis",
        "Create a chart showing revenue analysis by month for 2024",
        "Create a scatter plot of price vs quantity sold",
        "Create a heatmap showing sales by hour and day of week"
    ]
    
    console.print("[bold blue]Example Queries:[/bold blue]")
    for i, example in enumerate(examples, 1):
        console.print(f"{i}. {example}")
    
    console.print("\n[bold yellow]Usage:[/bold yellow]")
    console.print("chart-gen generate \"Your query here\"")
    console.print("chart-gen generate \"Create a bar chart of sales by type\" --csv-file data.csv")


def _display_results(result, verbose: bool) -> None:
    """Display generation results."""
    if result.success:
        console.print("[bold green]✅ Chart generation successful![/bold green]")
        
        # Show iteration info
        console.print(f"[blue]Iterations:[/blue] {result.iterations}")
        
        # Show generated code
        if verbose:
            console.print("\n[bold blue]Generated Code:[/bold blue]")
            console.print(Panel(result.final_code, title="Python Code"))
        
        # Show execution results
        if result.execution_result:
            if result.execution_result.success:
                console.print("[green]✅ Code executed successfully[/green]")
                if result.execution_result.generated_files:
                    console.print(f"[blue]Generated files:[/blue] {', '.join(result.execution_result.generated_files)}")
            else:
                console.print(f"[yellow]⚠️ Code execution failed:[/yellow] {result.execution_result.error}")
        
        # Show history if verbose
        if verbose and result.history:
            console.print("\n[bold blue]Reflection History:[/bold blue]")
            for i, entry in enumerate(result.history, 1):
                console.print(f"\n[bold]Iteration {i}:[/bold]")
                console.print(f"  Generator: {entry['generator_response']['explanation']}")
                console.print(f"  Critic: {entry['critique_response']['feedback']}")
                if entry['critique_response']['suggestions']:
                    console.print(f"  Suggestions: {', '.join(entry['critique_response']['suggestions'])}")
    
    else:
        console.print("[bold red]❌ Chart generation failed[/bold red]")
        if result.error_message:
            console.print(f"[red]Error:[/red] {result.error_message}")
        
        if verbose and result.history:
            console.print("\n[bold blue]Attempt History:[/bold blue]")
            for i, entry in enumerate(result.history, 1):
                console.print(f"\n[bold]Iteration {i}:[/bold]")
                console.print(f"  Generator: {entry['generator_response']['explanation']}")
                console.print(f"  Critic: {entry['critique_response']['feedback']}")


if __name__ == "__main__":
    cli()
