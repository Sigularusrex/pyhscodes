#!/usr/bin/env python3
"""Simple test to verify the basic fix works."""

import sys
import os

# Add the src directory to the path so we can import pyhscodes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    import pyhscodes

    print("Testing basic import and loading...")
    print(f"Loaded {len(pyhscodes.hscodes)} HS codes")
    print(f"Loaded {len(pyhscodes.sections)} sections")

    # Test basic lookup
    code = pyhscodes.hscodes.get(hscode="01")
    print(f"Found code: {code.hscode} - {code.description}")

    print("✅ All tests passed - no more AttributeError!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
