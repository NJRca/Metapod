#!/usr/bin/env python3
"""
Metapod CLI - Command Line Interface for the autonomous refactoring agent
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from metapod import MetapodAgent
from config import DEFAULT_CONFIG


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def print_banner():
    """Print Metapod banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    __  __      _                       _                     ║
║   |  \/  | ___| |_ __ _ _ __   ___   __| |                    ║
║   | |\/| |/ _ \ __/ _` | '_ \ / _ \ / _` |                    ║
║   | |  | |  __/ || (_| | |_) | (_) | (_| |                   ║
║   |_|  |_|\___|\__\__,_| .__/ \___/ \__,_|                   ║
║                        |_|                                   ║
║                                                              ║
║           Autonomous Backend Refactor & Hardening Agent     ║
║                      Claude Sonnet 4                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def run_autonomous_mode(project_path: str, request: str, config_file: str = None):
    """Run Metapod in autonomous mode"""
    print_banner()
    print(f"🚀 Starting autonomous refactoring for: {project_path}")
    print(f"📝 Request: {request}")
    print("=" * 70)
    
    # Load configuration if provided
    config = DEFAULT_CONFIG
    if config_file and Path(config_file).exists():
        print(f"📋 Loading configuration from: {config_file}")
    
    # Initialize and run agent
    agent = MetapodAgent(project_path)
    
    try:
        result = await agent.run(request)
        
        print("\n" + "=" * 70)
        print("✅ AUTONOMOUS REFACTORING COMPLETED")
        print("=" * 70)
        print(result)
        print("\n" + agent.get_todo_status())
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ AUTONOMOUS REFACTORING FAILED")
        print("=" * 70)
        print(f"Error: {str(e)}")
        logging.exception("Full error details:")
        
        return False


async def run_interactive_mode(project_path: str):
    """Run Metapod in interactive mode"""
    print_banner()
    print("🔄 Interactive Mode - Type 'help' for commands, 'exit' to quit")
    
    agent = MetapodAgent(project_path)
    
    while True:
        try:
            command = input("\nmetapod> ").strip()
            
            if command.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            elif command.lower() == 'help':
                print_help()
            elif command.lower() == 'status':
                print(agent.get_todo_status())
            elif command.lower() == 'research':
                topic = input("Research topic: ").strip()
                if topic:
                    print(f"🔍 Researching: {topic}")
                    # This would trigger research
                    print("Research completed (placeholder)")
            elif command.lower().startswith('refactor'):
                parts = command.split(' ', 1)
                request = parts[1] if len(parts) > 1 else "Begin autonomous refactoring"
                
                print(f"🔧 Starting refactoring: {request}")
                result = await agent.run(request)
                print(result)
                print(agent.get_todo_status())
            else:
                print("❓ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def print_help():
    """Print help information"""
    help_text = """
🔧 Metapod Commands:

  help        - Show this help message
  status      - Show current TODO status
  research    - Research a specific topic
  refactor    - Start autonomous refactoring
  exit/quit   - Exit interactive mode

🎯 Examples:
  metapod> refactor implement hexagonal architecture
  metapod> research latest fastapi patterns
  metapod> status
  
📚 Autonomous Mode:
  python cli.py /path/to/project "Implement error handling"
  
⚙️  Configuration:
  Use --config to specify custom configuration file
  Use --verbose for detailed logging
  Use --dry-run to see planned changes without execution
    """
    print(help_text)


async def validate_project(project_path: str) -> bool:
    """Validate that the project path is suitable for refactoring"""
    path = Path(project_path)
    
    if not path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        return False
    
    if not path.is_dir():
        print(f"❌ Project path is not a directory: {project_path}")
        return False
    
    # Check for common project indicators
    indicators = [
        "package.json",
        "requirements.txt", 
        "go.mod",
        "Cargo.toml",
        "pom.xml",
        "build.gradle",
        ".git"
    ]
    
    has_indicator = any((path / indicator).exists() for indicator in indicators)
    
    if not has_indicator:
        print(f"⚠️  Warning: No common project files found in {project_path}")
        print("This might not be a software project directory.")
        
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        return confirm == 'y'
    
    print(f"✅ Valid project detected: {project_path}")
    return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Metapod - Autonomous Backend Refactor & Hardening Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Autonomous mode
  python cli.py /path/to/project "Implement hexagonal architecture"
  
  # Interactive mode  
  python cli.py /path/to/project --interactive
  
  # With custom config
  python cli.py /path/to/project --config metapod.yaml "Add error handling"
  
  # Dry run mode
  python cli.py /path/to/project --dry-run "Refactor validation"
        """
    )
    
    parser.add_argument(
        "project_path",
        help="Path to the project to refactor"
    )
    
    parser.add_argument(
        "request",
        nargs="?",
        default="Begin autonomous refactoring",
        help="Refactoring request (default: 'Begin autonomous refactoring')"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--config", "-c",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without executing them"
    )
    
    parser.add_argument(
        "--register-vscode",
        action="store_true",
        help="Register Metapod as a VSCode agent"
    )
    
    parser.add_argument(
        "--vscode-task",
        action="store_true", 
        help="Generate VSCode task definitions"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Metapod 1.0.0 (Claude Sonnet 4)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Validate project path
    if not asyncio.run(validate_project(args.project_path)):
        sys.exit(1)
    
    try:
        if args.register_vscode:
            from vscode_agent import register_with_vscode
            success = register_with_vscode()
            sys.exit(0 if success else 1)
        
        if args.vscode_task:
            from vscode_agent import create_vscode_task_definition
            import json
            tasks = create_vscode_task_definition()
            print(json.dumps(tasks, indent=2))
            return
        
        if args.dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
            # In dry run, we would show planned changes
            print("Planned changes would be displayed here...")
            return
        
        if args.interactive:
            success = asyncio.run(run_interactive_mode(args.project_path))
        else:
            success = asyncio.run(run_autonomous_mode(
                args.project_path, 
                args.request, 
                args.config
            ))
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        if args.verbose:
            logging.exception("Full error details:")
        sys.exit(1)


if __name__ == "__main__":
    main()
