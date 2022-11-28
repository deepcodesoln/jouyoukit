"""This module provides facilities for persistent paths used by the jouyou toolkit."""

import os

"""
The folder the jouyou toolkit writes persistent information into. It should be expanded
before use.
"""
JYK_USER_DIR = "~/.jouyoukit"


def create_persistent_jyk_paths():
    """Create the persistent paths, if non-existent, used by the jouyou toolkit."""
    os.makedirs(os.path.expanduser(JYK_USER_DIR), exist_ok=True)
