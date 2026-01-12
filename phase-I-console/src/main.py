"""Entry point for the todo console application."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli import run_cli


def main() -> None:
    """Start the todo console application."""
    run_cli()


if __name__ == "__main__":
    main()
