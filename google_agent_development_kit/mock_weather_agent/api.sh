#!/bin/bash

# Weather API helper script
# Usage: ./api.sh [METHOD] [ENDPOINT] [DATA...]
# Examples:
#   ./api.sh GET /health
#   ./api.sh POST /weather message="test" location="NYC"

if [ $# -eq 0 ]; then
    echo "Usage: $0 [METHOD] [ENDPOINT] [DATA...]"
    echo "Examples:"
    echo "  $0 GET /health"
    echo "  $0 POST /weather message=\"test\" location=\"NYC\""
    exit 1
fi

METHOD=$1
ENDPOINT=$2
shift 2

# Use xh with localhost shorthand and pass all remaining arguments
echo "Executing: xh $METHOD :8000$ENDPOINT $@"
xh $METHOD :8000$ENDPOINT "$@"
