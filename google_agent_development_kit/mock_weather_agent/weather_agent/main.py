#!/usr/bin/env python3
"""
Weather Bot Agent Team - Main Entry Point

This script demonstrates the complete weather bot agent team from the Google ADK tutorial.
It includes all features from Steps 1-6:
- Basic weather lookup
- Multi-model support (Gemini, GPT-4o, Claude)
- Agent delegation (greeting/farewell sub-agents)
- Session state for memory
- Input and tool execution guardrails

Usage:
    python -m multi_tool_agent.main [--step STEP] [--model MODEL]
    
Options:
    --step STEP    Run a specific step (1-6) or 'all' for complete demo (default: all)
    --model MODEL  Choose model: gemini, gpt, or claude (default: gemini)
    
Examples:
    python -m multi_tool_agent.main                    # Run complete demo
    python -m multi_tool_agent.main --step 1           # Run Step 1 only
    python -m multi_tool_agent.main --step 4 --model gpt  # Run Step 4 with GPT-4o
"""

import asyncio
import argparse
from weather_agent.agent import (
    test_step1_basic_weather,
    test_step2_multi_model,
    test_step3_agent_team,
    test_step4_stateful_memory,
    test_step5_input_guardrail,
    test_step6_tool_guardrail,
    run_complete_demo
)


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


async def main():
    """Main function to run the weather bot agent team demo."""
    parser = argparse.ArgumentParser(
        description="Weather Bot Agent Team - Demonstrating ADK features",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--step",
        type=str,
        default="all",
        choices=["1", "2", "3", "4", "5", "6", "all"],
        help="Which step to run (1-6) or 'all' for complete demo"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gemini",
        choices=["gemini", "gpt", "claude"],
        help="Which model to use (only affects steps that support multiple models)"
    )
    
    args = parser.parse_args()
    
    print_header("🌦️  WEATHER BOT AGENT TEAM  🌦️")
    print("Welcome to the Weather Bot Agent Team demonstration!")
    print("This showcases various ADK features through a progressive tutorial.\n")
    
    if args.step == "1":
        print_header("Step 1: Basic Weather Agent")
        print("Creating a simple agent that can look up weather information...")
        await test_step1_basic_weather()
        
    elif args.step == "2":
        print_header("Step 2: Multi-Model Support with LiteLLM")
        print("Testing the same agent logic with different LLMs...")
        await test_step2_multi_model()
        
    elif args.step == "3":
        print_header("Step 3: Agent Team with Delegation")
        print("Creating specialized sub-agents for greetings and farewells...")
        await test_step3_agent_team()
        
    elif args.step == "4":
        print_header("Step 4: Memory and Personalization")
        print("Using session state to remember user preferences...")
        await test_step4_stateful_memory()
        
    elif args.step == "5":
        print_header("Step 5: Input Guardrail")
        print("Implementing safety checks before messages reach the model...")
        await test_step5_input_guardrail()
        
    elif args.step == "6":
        print_header("Step 6: Tool Execution Guardrail")
        print("Controlling tool execution based on arguments...")
        await test_step6_tool_guardrail()
        
    else:  # args.step == "all"
        print_header("Complete Weather Bot Team Demo")
        print("Running all features in a comprehensive demonstration...")
        await run_complete_demo()
    
    print("\n" + "="*70)
    print("  Demo completed! Thank you for exploring ADK.")
    print("="*70 + "\n")


def run():
    """Entry point for the script."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        raise


if __name__ == "__main__":
    run()