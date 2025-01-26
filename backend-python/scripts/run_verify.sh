#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."
PYTHONPATH=$PYTHONPATH:$(pwd) python scripts/verify_data.py 