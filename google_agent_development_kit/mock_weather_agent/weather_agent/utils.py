"""Utility functions for the weather agent."""

import warnings
import sys
import os
from contextlib import contextmanager
from io import StringIO


@contextmanager
def suppress_adk_warnings():
    """Context manager to suppress ADK's function_call warnings."""
    # Capture warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", 
                              message="there are non-text parts in the response", 
                              category=UserWarning)
        
        # Also capture stderr to suppress printed warnings
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        try:
            yield
        finally:
            # Check if the captured output contains the warning we want to suppress
            captured = sys.stderr.getvalue()
            sys.stderr = old_stderr
            
            # Only print lines that don't contain our specific warning
            for line in captured.splitlines():
                if "there are non-text parts in the response" not in line:
                    print(line, file=sys.stderr)