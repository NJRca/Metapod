#!/usr/bin/env python3
"""
Metapod - One-liner setup and execution script
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Quick execution of Metapod"""
    if len(sys.argv) < 2:
        print("Usage: ./run_metapod.py <project_path> [request]")
        print("Example: ./run_metapod.py ./my-project 'Add error handling'")
        sys.exit(1)
    
    # Ensure dependencies are installed
    try:
        import aiohttp
        import yaml
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run the CLI
    args = [sys.executable, "cli.py"] + sys.argv[1:]
    subprocess.run(args)


if __name__ == "__main__":
    main()
