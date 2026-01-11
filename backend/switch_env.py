#!/usr/bin/env python
"""
Environment Switcher for Dogger 2.0
Quickly switch between development, staging, and production environments
"""

import shutil
import sys
from pathlib import Path


def switch_environment(env):
    """Switch to specified environment"""
    env_files = {
        'dev': '.env.development',
        'development': '.env.development',
        'staging': '.env.staging',
        'prod': '.env.production',
        'production': '.env.production',
    }
    
    if env.lower() not in env_files:
        print(f"❌ Invalid environment: {env}")
        print(f"Valid options: {', '.join(set(env_files.keys()))}")
        sys.exit(1)
    
    source_file = Path(env_files[env.lower()])
    target_file = Path('.env')
    
    if not source_file.exists():
        print(f"❌ Environment file not found: {source_file}")
        print(f"Please create {source_file} first")
        sys.exit(1)
    
    # Backup current .env
    if target_file.exists():
        backup_file = Path('.env.backup')
        shutil.copy(target_file, backup_file)
        print(f"📦 Backed up current .env to .env.backup")
    
    # Copy environment file
    shutil.copy(source_file, target_file)
    print(f"✅ Switched to {env.upper()} environment")
    print(f"📄 Copied {source_file} → .env")
    print()
    
    # Show current environment
    print("🔍 Current Environment Settings:")
    with open(target_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Mask sensitive values
                if any(key in line.upper() for key in ['PASSWORD', 'SECRET', 'KEY', 'TOKEN']):
                    key = line.split('=')[0]
                    print(f"  {key}=***REDACTED***")
                else:
                    print(f"  {line}")
    print()
    print("⚠️  Remember to restart your Django server!")


def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("🔄 DOGGER 2.0 - ENVIRONMENT SWITCHER")
        print("=" * 70)
        print()
        print("Usage: python switch_env.py <environment>")
        print()
        print("Available environments:")
        print("  • dev / development  - Local development")
        print("  • staging           - Staging server")
        print("  • prod / production - Production server")
        print()
        print("Example:")
        print("  python switch_env.py dev")
        print("  python switch_env.py production")
        print()
        sys.exit(1)
    
    env = sys.argv[1]
    switch_environment(env)


if __name__ == '__main__':
    main()