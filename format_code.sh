#!/bin/bash
# Format code with black
# Usage: ./format_code.sh

echo "Formatting code with black..."
black --line-length 100 my_rdbms/ tests/
echo "✓ Code formatting complete!"
