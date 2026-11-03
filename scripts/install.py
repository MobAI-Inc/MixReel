#!/usr/bin/env python3
"""Install the seven MixReel skills into an agent skills directory."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_collection import main

if __name__ == "__main__":
    main()
