#!/usr/bin/env python
"""
Secret Key Generator for Dogger 2.0
Generates secure SECRET_KEY and JWT signing keys
"""

import secrets
import string


def generate_django_secret_key(length=50):
    """Generate a secure Django SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_jwt_key(length=64):
    """Generate a secure JWT signing key"""
    return secrets.token_urlsafe(length)


def main():
    print("=" * 70)
    print("🔐 DOGGER 2.0 - SECRET KEY GENERATOR")
    print("=" * 70)
    print()
    
    print("📝 Generated Keys (copy these to your .env file):")
    print()
    
    # Django Secret Key
    django_key = generate_django_secret_key()
    print("SECRET_KEY:")
    print(django_key)
    print()
    
    # JWT Signing Key
    jwt_key = generate_jwt_key()
    print("JWT_SIGNING_KEY:")
    print(jwt_key)
    print()
    
    print("=" * 70)
    print("⚠️  IMPORTANT SECURITY NOTES:")
    print("=" * 70)
    print()
    print("1. ✅ Copy these keys to your .env file")
    print("2. ✅ NEVER commit .env file to version control")
    print("3. ✅ Use different keys for production")
    print("4. ✅ Rotate keys periodically (every 90 days)")
    print("5. ✅ Keep backups of production keys securely")
    print()
    print("=" * 70)
    print()
    
    # Save to file option
    save = input("💾 Save keys to secrets.txt? (y/n): ").lower()
    if save == 'y':
        with open('secrets.txt', 'w') as f:
            f.write("# Dogger 2.0 - Generated Secrets\n")
            f.write("# DO NOT COMMIT THIS FILE!\n\n")
            f.write(f"SECRET_KEY={django_key}\n")
            f.write(f"JWT_SIGNING_KEY={jwt_key}\n")
        print("✅ Keys saved to secrets.txt")
        print("⚠️  Remember to add secrets.txt to .gitignore!")
    else:
        print("✅ Keys not saved. Copy them manually.")


if __name__ == '__main__':
    main()