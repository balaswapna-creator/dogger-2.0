#!/usr/bin/env python3
"""
Environment Switcher for Dogger 2.0
Switches between development and production .env files
"""
import os
import sys
import shutil
from pathlib import Path

def switch_environment(env_name):
    """
    Switch between development and production environments
    Args:
        env_name: 'development' or 'production'
    """
    # Get the backend directory
    backend_dir = Path(__file__).parent
    
    # Define file paths
    current_env = backend_dir / '.env'
    backup_env = backend_dir / '.env.backup'
    target_env = backend_dir / f'.env.{env_name}'
    
    # Check if target environment file exists
    if not target_env.exists():
        print(f"❌ Error: {target_env} does not exist!")
        print(f"📁 Please create .env.{env_name} file first")
        sys.exit(1)
    
    # Backup current .env if it exists
    if current_env.exists():
        shutil.copy(current_env, backup_env)
        print(f"📦 Backed up current .env to .env.backup")
    
    # Copy target environment file to .env
    shutil.copy(target_env, current_env)
    print(f"✅ Switched to {env_name.upper()} environment")
    print(f"📄 Copied .env.{env_name} → .env")
    
    # Display current settings
    print("\n🔍 Current Environment Settings:")
    try:
        # FIXED: Add encoding='utf-8' to handle Unicode characters
        with open(current_env, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                # Only show non-empty lines and non-comments
                if line and not line.startswith('#'):
                    # Hide sensitive values (show only key names)
                    if '=' in line:
                        key = line.split('=')[0]
                        print(f"  ✓ {key}")
    except Exception as e:
        print(f"⚠️  Could not read .env file: {e}")
    
    print(f"\n🎯 Now using {env_name.upper()} configuration")
    print(f"💡 Restart your Django server for changes to take effect")

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python switch_env.py [development|production]")
        print("\nExample:")
        print("  python switch_env.py development")
        print("  python switch_env.py production")
        sys.exit(1)
    
    env = sys.argv[1].lower()
    
    if env not in ['development', 'production']:
        print("❌ Error: Environment must be 'development' or 'production'")
        sys.exit(1)
    
    switch_environment(env)

if __name__ == '__main__':
    main()