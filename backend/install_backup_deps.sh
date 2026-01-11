#!/bin/bash

# Install Backup System Dependencies
# Week 4 Day 1: Backup system setup

echo "📦 Installing Backup System Dependencies..."
echo "==========================================="
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed"
    echo "   Please install pip first"
    exit 1
fi

echo "▶️  Installing Python packages..."
echo ""

# Install cryptography for encryption
echo "1/2 Installing cryptography..."
pip install cryptography
if [ $? -eq 0 ]; then
    echo "✅ cryptography installed"
else
    echo "❌ Failed to install cryptography"
    exit 1
fi

# Install schedule for automated backups
echo ""
echo "2/2 Installing schedule..."
pip install schedule
if [ $? -eq 0 ]; then
    echo "✅ schedule installed"
else
    echo "❌ Failed to install schedule"
    exit 1
fi

echo ""
echo "==========================================="
echo "✅ All dependencies installed successfully!"
echo ""
echo "📚 Next steps:"
echo "   1. Run: python test_backups.py"
echo "   2. Create first backup: python backup_manager.py create"
echo "   3. List backups: python backup_manager.py list"
echo ""
echo "📖 For more commands, run:"
echo "   python backup_manager.py"
echo "   python backup_scheduler.py"
echo ""