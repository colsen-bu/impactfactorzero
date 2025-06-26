#!/bin/bash
# Setup script for Impact Factor Zero blog environment

echo "🚀 Setting up Python virtual environment for Impact Factor Zero blog..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📦 Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found. Please create one with your dependencies."
fi

echo "✅ Virtual environment setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate the environment, run:"
echo "  deactivate"
