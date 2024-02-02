"""
Main app entry point.
"""

import sys
from pathlib import Path

from session import Session
MAIN_WORKSPACE = str(Path(__file__).parent)
sys.path.append(MAIN_WORKSPACE)
sys.path.append(MAIN_WORKSPACE + "\\ai_model")
sys.path.append(MAIN_WORKSPACE + "\\settings_readers")


def main():
    """Main function."""
    session = Session()
    session.start_session()


if __name__ == "__main__":
    main()
