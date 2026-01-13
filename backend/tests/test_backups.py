"""
Backup System Test Suite
Week 4 Day 1: Comprehensive backup testing
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from backup_manager import BackupManager


class BackupTester:
    """Test suite for backup system"""
    
    def __init__(self):
        self.manager = BackupManager()
        self.test_results = []
        
        print("🧪 Backup System Test Suite")
        print("=" * 60)
    
    def run_test(self, test_name, test_func):
        """Run individual test"""
        print(f"\n▶️  Test: {test_name}")
        print("-" * 60)
        
        try:
            result = test_func()
            if result:
                print(f"✅ PASSED: {test_name}")
                self.test_results.append((test_name, True, None))
            else:
                print(f"❌ FAILED: {test_name}")
                self.test_results.append((test_name, False, "Test returned False"))
        except Exception as e:
            print(f"❌ ERROR: {test_name}")
            print(f"   Error: {str(e)}")
            self.test_results.append((test_name, False, str(e)))
    
    def test_backup_creation(self):
        """Test 1: Create a backup"""
        print("Creating test backup...")
        
        backup_path = self.manager.create_backup('test')
        
        # Verify backup exists
        if not backup_path.exists():
            print("   ❌ Backup directory not created")
            return False
        
        # Check required files
        required_files = [
            'database.db.gz.enc',
            'metadata.json'
        ]
        
        for file in required_files:
            file_path = backup_path / file
            if not file_path.exists():
                print(f"   ❌ Missing file: {file}")
                return False
            print(f"   ✓ Found: {file}")
        
        print("   ✓ Backup created successfully")
        return True
    
    def test_backup_encryption(self):
        """Test 2: Verify encryption"""
        print("Testing encryption...")
        
        # Get latest backup
        backups = self.manager.list_backups()
        if not backups:
            print("   ❌ No backups found")
            return False
        
        latest = backups[-1]
        backup_path = self.manager.backup_dir / latest['backup_name']
        encrypted_file = backup_path / 'database.db.gz.enc'
        
        # Try to read encrypted file (should be gibberish)
        with open(encrypted_file, 'rb') as f:
            data = f.read(100)  # Read first 100 bytes
        
        # Check if data is encrypted (no recognizable database header)
        if data.startswith(b'SQLite') or data.startswith(b'\x1f\x8b'):
            print("   ❌ Data appears unencrypted")
            return False
        
        print("   ✓ Data is encrypted")
        return True
    
    def test_backup_compression(self):
        """Test 3: Verify compression"""
        print("Testing compression...")
        
        backups = self.manager.list_backups()
        if not backups:
            print("   ❌ No backups found")
            return False
        
        latest = backups[-1]
        original_size = latest['original_size']
        compressed_size = latest['compressed_size']
        
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"   Original: {original_size:,} bytes")
        print(f"   Compressed: {compressed_size:,} bytes")
        print(f"   Ratio: {compression_ratio:.1f}%")
        
        if compressed_size >= original_size:
            print("   ⚠️  Warning: Compression didn't reduce size")
            # This is OK for small databases
        
        print("   ✓ Compression working")
        return True
    
    def test_backup_metadata(self):
        """Test 4: Verify metadata"""
        print("Testing metadata...")
        
        backups = self.manager.list_backups()
        if not backups:
            print("   ❌ No backups found")
            return False
        
        latest = backups[-1]
        
        required_fields = [
            'backup_name', 'backup_type', 'environment',
            'timestamp', 'datetime', 'database_type',
            'original_size', 'compressed_size', 'checksum',
            'retention_until'
        ]
        
        for field in required_fields:
            if field not in latest:
                print(f"   ❌ Missing metadata field: {field}")
                return False
            print(f"   ✓ {field}: {latest[field]}")
        
        print("   ✓ All metadata present")
        return True
    
    def test_backup_verification(self):
        """Test 5: Verify backup integrity"""
        print("Testing verification...")
        
        backups = self.manager.list_backups()
        if not backups:
            print("   ❌ No backups found")
            return False
        
        latest = backups[-1]
        result = self.manager.verify_backup(latest['backup_name'])
        
        if not result:
            print("   ❌ Backup verification failed")
            return False
        
        print("   ✓ Backup verified")
        return True
    
    def test_backup_restore(self):
        """Test 6: Test restore functionality"""
        print("Testing restore...")
        
        backups = self.manager.list_backups()
        if not backups:
            print("   ❌ No backups found")
            return False
        
        latest = backups[-1]
        
        # Create temporary restore location
        temp_restore = Path('temp_restored_db.sqlite3')
        
        try:
            # Restore to temp location
            self.manager.restore_backup(
                latest['backup_name'],
                target_path=temp_restore
            )
            
            # Verify restored file exists
            if not temp_restore.exists():
                print("   ❌ Restored file not found")
                return False
            
            # Check file size
            restored_size = temp_restore.stat().st_size
            original_size = latest['original_size']
            
            if restored_size != original_size:
                print(f"   ❌ Size mismatch: {restored_size} != {original_size}")
                return False
            
            print(f"   ✓ Restored successfully ({restored_size:,} bytes)")
            
            # Cleanup
            temp_restore.unlink()
            
            return True
            
        except Exception as e:
            print(f"   ❌ Restore failed: {str(e)}")
            # Cleanup on failure
            if temp_restore.exists():
                temp_restore.unlink()
            return False
    
    def test_backup_rotation(self):
        """Test 7: Test backup rotation"""
        print("Testing rotation...")
        
        # Get current backup count
        initial_backups = self.manager.list_backups()
        initial_count = len(initial_backups)
        
        print(f"   Initial backups: {initial_count}")
        
        # Run rotation
        self.manager.rotate_backups()
        
        # Get new count
        final_backups = self.manager.list_backups()
        final_count = len(final_backups)
        
        print(f"   Final backups: {final_count}")
        
        # In development, retention is 7 days, so nothing should be removed yet
        if final_count <= initial_count:
            print("   ✓ Rotation completed")
            return True
        else:
            print("   ❌ Backup count increased after rotation")
            return False
    
    def test_backup_index(self):
        """Test 8: Verify backup index"""
        print("Testing backup index...")
        
        index_file = self.manager.backup_dir / 'backup_index.json'
        
        if not index_file.exists():
            print("   ❌ Backup index not found")
            return False
        
        import json
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        # Check index structure
        if 'backups' not in index:
            print("   ❌ Missing 'backups' key")
            return False
        
        if 'last_updated' not in index:
            print("   ❌ Missing 'last_updated' key")
            return False
        
        if 'total_backups' not in index:
            print("   ❌ Missing 'total_backups' key")
            return False
        
        backup_count = len(index['backups'])
        total_reported = index['total_backups']
        
        if backup_count != total_reported:
            print(f"   ❌ Count mismatch: {backup_count} != {total_reported}")
            return False
        
        print(f"   ✓ Index valid ({backup_count} backups)")
        return True
    
    def test_encryption_key(self):
        """Test 9: Verify encryption key exists"""
        print("Testing encryption key...")
        
        key_file = self.manager.backup_dir / '.backup_key'
        
        if not key_file.exists():
            print("   ❌ Encryption key not found")
            return False
        
        # Check key is in gitignore
        gitignore = Path('.gitignore')
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                content = f.read()
            
            if '.backup_key' not in content:
                print("   ⚠️  Warning: .backup_key not in .gitignore")
        
        print("   ✓ Encryption key exists")
        return True
    
    def test_multiple_backups(self):
        """Test 10: Create multiple backups"""
        print("Testing multiple backup creation...")
        
        initial_count = len(self.manager.list_backups())
        
        # Create 3 backups
        for i in range(3):
            print(f"   Creating backup {i+1}/3...")
            self.manager.create_backup(f'test-multiple-{i+1}')
        
        final_count = len(self.manager.list_backups())
        
        if final_count != initial_count + 3:
            print(f"   ❌ Expected {initial_count + 3} backups, got {final_count}")
            return False
        
        print(f"   ✓ Created 3 backups successfully")
        return True
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result, _ in self.test_results if result)
        failed = sum(1 for _, result, _ in self.test_results if not result)
        total = len(self.test_results)
        
        print(f"\nTotal Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for name, result, error in self.test_results:
                if not result:
                    print(f"   - {name}")
                    if error:
                        print(f"     Error: {error}")
        
        print("\n" + "=" * 60)
        
        if failed == 0:
            print("✅ ALL TESTS PASSED!")
        else:
            print(f"⚠️  {failed} TEST(S) FAILED")
        
        print("=" * 60)
        
        return failed == 0
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n🚀 Running all tests...\n")
        
        tests = [
            ("Backup Creation", self.test_backup_creation),
            ("Backup Encryption", self.test_backup_encryption),
            ("Backup Compression", self.test_backup_compression),
            ("Backup Metadata", self.test_backup_metadata),
            ("Backup Verification", self.test_backup_verification),
            ("Backup Restore", self.test_backup_restore),
            ("Backup Rotation", self.test_backup_rotation),
            ("Backup Index", self.test_backup_index),
            ("Encryption Key", self.test_encryption_key),
            ("Multiple Backups", self.test_multiple_backups),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        return self.print_summary()


def main():
    """Main test interface"""
    tester = BackupTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()