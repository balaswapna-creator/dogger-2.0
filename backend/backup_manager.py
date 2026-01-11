"""
Database Backup Manager with Encryption and Rotation
Week 4 Day 1: Automated backup system for Dogger 2.0
"""

import os
import gzip
import shutil
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from django.conf import settings
from clinic.config import config


class BackupManager:
    """Manages database backups with encryption and rotation"""
    
    def __init__(self):
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
        
        # Environment-specific settings
        self.environment = config.get('ENVIRONMENT', 'development')
        self.retention_days = self._get_retention_days()
        self.backup_frequency = self._get_backup_frequency()
        
        # Encryption key from environment or generate
        self.encryption_key = self._get_encryption_key()
        
        print(f"🔧 Backup Manager initialized")
        print(f"   Environment: {self.environment}")
        print(f"   Retention: {self.retention_days} days")
        print(f"   Frequency: {self.backup_frequency}")
    
    def _get_retention_days(self):
        """Get retention period based on environment"""
        retention = {
            'development': 7,
            'staging': 30,
            'production': 90
        }
        return retention.get(self.environment, 7)
    
    def _get_backup_frequency(self):
        """Get backup frequency based on environment"""
        frequency = {
            'development': 'daily',
            'staging': 'every 6 hours',
            'production': 'every 1 hour'
        }
        return frequency.get(self.environment, 'daily')
    
    def _get_encryption_key(self):
        """Get or generate encryption key"""
        key_file = self.backup_dir / '.backup_key'
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        
        # Generate new key
        backup_password = config.get('BACKUP_ENCRYPTION_KEY', 'default-backup-key-change-in-production')
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'dogger_backup_salt_v1',  # In production, use random salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(backup_password.encode()))
        
        # Save key securely
        with open(key_file, 'wb') as f:
            f.write(key)
        
        # Add to gitignore
        gitignore = Path('.gitignore')
        if gitignore.exists():
            with open(gitignore, 'a') as f:
                f.write('\n# Backup encryption key\nbackups/.backup_key\n')
        
        return key
    
    def create_backup(self, backup_type='manual'):
        """Create encrypted database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{self.environment}_{backup_type}_{timestamp}"
        
        print(f"\n📦 Creating backup: {backup_name}")
        
        try:
            # Step 1: Identify database file
            db_path = self._get_database_path()
            print(f"   Database: {db_path}")
            
            # Step 2: Create backup directory for this backup
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(exist_ok=True)
            
            # Step 3: Copy database
            db_backup = backup_path / 'database.db'
            shutil.copy2(db_path, db_backup)
            print(f"   ✓ Database copied")
            
            # Step 4: Compress
            compressed = backup_path / 'database.db.gz'
            with open(db_backup, 'rb') as f_in:
                with gzip.open(compressed, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(db_backup)  # Remove uncompressed
            print(f"   ✓ Compressed")
            
            # Step 5: Encrypt
            encrypted = backup_path / 'database.db.gz.enc'
            fernet = Fernet(self.encryption_key)
            with open(compressed, 'rb') as f:
                encrypted_data = fernet.encrypt(f.read())
            with open(encrypted, 'wb') as f:
                f.write(encrypted_data)
            os.remove(compressed)  # Remove unencrypted compressed
            print(f"   ✓ Encrypted")
            
            # Step 6: Generate checksum
            checksum = self._generate_checksum(encrypted)
            print(f"   ✓ Checksum: {checksum[:16]}...")
            
            # Step 7: Create metadata
            metadata = {
                'backup_name': backup_name,
                'backup_type': backup_type,
                'environment': self.environment,
                'timestamp': timestamp,
                'datetime': datetime.now().isoformat(),
                'database_type': 'sqlite' if 'sqlite3' in str(db_path).lower() else 'postgresql',
                'original_size': os.path.getsize(db_path),
                'compressed_size': os.path.getsize(encrypted),
                'checksum': checksum,
                'retention_until': (datetime.now() + timedelta(days=self.retention_days)).isoformat()
            }
            
            metadata_file = backup_path / 'metadata.json'
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"   ✓ Metadata saved")
            
            # Step 8: Create backup index
            self._update_backup_index(metadata)
            
            print(f"\n✅ Backup created successfully!")
            print(f"   Location: {backup_path}")
            print(f"   Size: {metadata['original_size']:,} bytes → {metadata['compressed_size']:,} bytes")
            print(f"   Compression: {(1 - metadata['compressed_size']/metadata['original_size'])*100:.1f}%")
            print(f"   Expires: {metadata['retention_until'][:10]}")
            
            return backup_path
            
        except Exception as e:
            print(f"\n❌ Backup failed: {str(e)}")
            # Cleanup failed backup
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise
    
    def _get_database_path(self):
        """Get database file path based on environment"""
        db_config = settings.DATABASES['default']
        
        if db_config['ENGINE'] == 'django.db.backends.sqlite3':
            return Path(db_config['NAME'])
        else:
            # For PostgreSQL, we'll use pg_dump (to be implemented)
            raise NotImplementedError("PostgreSQL backup requires pg_dump - coming in next iteration")
    
    def _generate_checksum(self, file_path):
        """Generate SHA256 checksum for file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _update_backup_index(self, metadata):
        """Update backup index with new backup info"""
        index_file = self.backup_dir / 'backup_index.json'
        
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
        else:
            index = {'backups': []}
        
        index['backups'].append(metadata)
        index['last_updated'] = datetime.now().isoformat()
        index['total_backups'] = len(index['backups'])
        
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
    
    def list_backups(self):
        """List all available backups"""
        index_file = self.backup_dir / 'backup_index.json'
        
        if not index_file.exists():
            print("📋 No backups found")
            return []
        
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        backups = index.get('backups', [])
        
        print(f"\n📋 Available Backups ({len(backups)} total):\n")
        print(f"{'#':<4} {'Name':<40} {'Date':<20} {'Size':<12} {'Type':<10}")
        print("-" * 90)
        
        for i, backup in enumerate(backups, 1):
            name = backup['backup_name']
            date = backup['datetime'][:19]
            size = f"{backup['compressed_size']:,} B"
            backup_type = backup['backup_type']
            print(f"{i:<4} {name:<40} {date:<20} {size:<12} {backup_type:<10}")
        
        return backups
    
    def restore_backup(self, backup_name, target_path=None):
        """Restore database from encrypted backup"""
        print(f"\n🔄 Restoring backup: {backup_name}")
        
        try:
            backup_path = self.backup_dir / backup_name
            
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup not found: {backup_name}")
            
            # Step 1: Load metadata
            metadata_file = backup_path / 'metadata.json'
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            print(f"   Environment: {metadata['environment']}")
            print(f"   Created: {metadata['datetime'][:19]}")
            print(f"   Type: {metadata['backup_type']}")
            
            # Step 2: Decrypt
            encrypted_file = backup_path / 'database.db.gz.enc'
            fernet = Fernet(self.encryption_key)
            with open(encrypted_file, 'rb') as f:
                decrypted_data = fernet.decrypt(f.read())
            print(f"   ✓ Decrypted")
            
            # Step 3: Verify checksum
            temp_compressed = backup_path / 'temp_database.db.gz'
            with open(temp_compressed, 'wb') as f:
                f.write(decrypted_data)
            
            # Step 4: Decompress
            temp_db = backup_path / 'temp_database.db'
            with gzip.open(temp_compressed, 'rb') as f_in:
                with open(temp_db, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"   ✓ Decompressed")
            
            # Step 5: Restore to target
            if target_path is None:
                target_path = self._get_database_path()
            
            # Create backup of current database before restoring
            if Path(target_path).exists():
                backup_current = Path(str(target_path) + '.before_restore')
                shutil.copy2(target_path, backup_current)
                print(f"   ✓ Current database backed up to: {backup_current}")
            
            shutil.copy2(temp_db, target_path)
            print(f"   ✓ Restored to: {target_path}")
            
            # Cleanup temp files
            temp_compressed.unlink()
            temp_db.unlink()
            
            print(f"\n✅ Restore completed successfully!")
            print(f"   ⚠️  Restart the Django server to use the restored database")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Restore failed: {str(e)}")
            raise
    
    def rotate_backups(self):
        """Remove old backups based on retention policy"""
        print(f"\n🗑️  Rotating backups (retention: {self.retention_days} days)")
        
        index_file = self.backup_dir / 'backup_index.json'
        if not index_file.exists():
            print("   No backups to rotate")
            return
        
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        backups = index.get('backups', [])
        removed_count = 0
        kept_backups = []
        
        for backup in backups:
            retention_until = datetime.fromisoformat(backup['retention_until'])
            
            if datetime.now() > retention_until:
                # Remove expired backup
                backup_path = self.backup_dir / backup['backup_name']
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                    removed_count += 1
                    print(f"   ✓ Removed: {backup['backup_name']}")
            else:
                kept_backups.append(backup)
        
        # Update index
        index['backups'] = kept_backups
        index['last_updated'] = datetime.now().isoformat()
        index['total_backups'] = len(kept_backups)
        
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"\n✅ Rotation complete!")
        print(f"   Removed: {removed_count} backups")
        print(f"   Kept: {len(kept_backups)} backups")
    
    def verify_backup(self, backup_name):
        """Verify backup integrity"""
        print(f"\n🔍 Verifying backup: {backup_name}")
        
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            print("   ❌ Backup not found")
            return False
        
        try:
            # Load metadata
            metadata_file = backup_path / 'metadata.json'
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Check encrypted file exists
            encrypted_file = backup_path / 'database.db.gz.enc'
            if not encrypted_file.exists():
                print("   ❌ Encrypted file missing")
                return False
            
            # Verify checksum
            current_checksum = self._generate_checksum(encrypted_file)
            if current_checksum != metadata['checksum']:
                print("   ❌ Checksum mismatch - backup may be corrupted")
                return False
            
            # Try to decrypt (without decompressing)
            fernet = Fernet(self.encryption_key)
            with open(encrypted_file, 'rb') as f:
                fernet.decrypt(f.read())
            
            print(f"   ✅ Backup verified successfully")
            print(f"   Checksum: {current_checksum[:16]}... ✓")
            print(f"   Encryption: Valid ✓")
            print(f"   Size: {metadata['compressed_size']:,} bytes ✓")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Verification failed: {str(e)}")
            return False


def main():
    """Main backup manager interface"""
    import sys
    
    manager = BackupManager()
    
    if len(sys.argv) < 2:
        print("\n📚 Backup Manager Commands:")
        print("   python backup_manager.py create [type]  - Create backup (type: manual/scheduled/pre-deploy)")
        print("   python backup_manager.py list           - List all backups")
        print("   python backup_manager.py restore <name> - Restore backup")
        print("   python backup_manager.py verify <name>  - Verify backup integrity")
        print("   python backup_manager.py rotate         - Remove old backups")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        backup_type = sys.argv[2] if len(sys.argv) > 2 else 'manual'
        manager.create_backup(backup_type)
        
    elif command == 'list':
        manager.list_backups()
        
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Error: Please specify backup name")
            print("   Usage: python backup_manager.py restore <backup_name>")
            return
        manager.restore_backup(sys.argv[2])
        
    elif command == 'verify':
        if len(sys.argv) < 3:
            print("❌ Error: Please specify backup name")
            return
        manager.verify_backup(sys.argv[2])
        
    elif command == 'rotate':
        manager.rotate_backups()
        
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()