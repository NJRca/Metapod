#!/bin/bash
# Metapod Setup Script
# Quick setup for the autonomous refactoring agent

echo "🚀 Setting up Metapod - Autonomous Backend Refactor & Hardening Agent"
echo "=================================================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version detected"

# Install dependencies
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Make scripts executable
chmod +x cli.py
chmod +x run_metapod.py
chmod +x demo.py
echo "✅ Scripts made executable"

# Run a quick test
echo "🧪 Running quick validation..."
python3 -c "from metapod import MetapodAgent; print('✅ Metapod imports successfully')" || {
    echo "❌ Import test failed"
    exit 1
}

echo ""
echo "🎉 Metapod setup complete!"
echo ""
echo "Quick Start:"
echo "  # Autonomous mode"
echo "  python3 cli.py /path/to/project 'Add error handling'"
echo ""  
echo "  # Interactive mode"
echo "  python3 cli.py /path/to/project --interactive"
echo ""
echo "  # Demo"
echo "  python3 demo.py"
echo ""
echo "  # One-liner"
echo "  ./run_metapod.py /path/to/project 'Refactor request'"
echo ""
echo "Documentation: https://github.com/NJRca/Metapod"
echo "Happy refactoring! 🛡️→🦋"
