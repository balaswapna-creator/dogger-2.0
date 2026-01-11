"""
Automated Backup Scheduler
Week 4 Day 1: Schedule backups based on environment
"""

import os
import time
import schedule
from datetime import datetime
from backup_manager import BackupManager

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from clinic.config import config


class BackupScheduler:
    """Automated backup scheduling based on environment"""
    
    def __init__(self):
        self.manager = BackupManager()
        self.environment = config.get('ENVIRONMENT', 'development')
        self.running = False
        
        print(f"⏰ Backup Scheduler initialized")
        print(f"   Environment: {self.environment}")
    
    def schedule_backups(self):
        """Setup backup schedule based on environment"""
        schedule.clear()
        
        if self.environment == 'production':
            # Production: Hourly backups + daily rotation
            schedule.every().hour.do(self._create_scheduled_backup)
            schedule.every().day.at("02:00").do(self._rotate_backups)
            schedule.every().day.at("03:00").do(self._verify_recent_backups)
            print("   📅 Schedule: Hourly backups, daily rotation at 2 AM")
            
        elif self.environment == 'staging':
            # Staging: Every 6 hours + weekly rotation
            schedule.every(6).hours.do(self._create_scheduled_backup)
            schedule.every().sunday.at("02:00").do(self._rotate_backups)
            schedule.every().monday.at("03:00").do(self._verify_recent_backups)
            print("   📅 Schedule: Every 6 hours, weekly rotation on Sunday")
            
        else:  # development
            # Development: Daily backups at midnight
            schedule.every().day.at("00:00").do(self._create_scheduled_backup)
            schedule.every().monday.at("01:00").do(self._rotate_backups)
            print("   📅 Schedule: Daily at midnight, weekly rotation on Monday")
    
    def _create_scheduled_backup(self):
        """Create scheduled backup"""
        print(f"\n⏰ Scheduled backup triggered at {datetime.now()}")
        try:
            self.manager.create_backup('scheduled')
            return True
        except Exception as e:
            print(f"❌ Scheduled backup failed: {str(e)}")
            # TODO: Send alert to administrators
            return False
    
    def _rotate_backups(self):
        """Rotate old backups"""
        print(f"\n⏰ Scheduled rotation triggered at {datetime.now()}")
        try:
            self.manager.rotate_backups()
            return True
        except Exception as e:
            print(f"❌ Scheduled rotation failed: {str(e)}")
            return False
    
    def _verify_recent_backups(self):
        """Verify recent backups"""
        print(f"\n⏰ Scheduled verification triggered at {datetime.now()}")
        try:
            backups = self.manager.list_backups()
            # Verify last 3 backups
            recent = backups[-3:] if len(backups) >= 3 else backups
            
            verified = 0
            failed = 0
            
            for backup in recent:
                if self.manager.verify_backup(backup['backup_name']):
                    verified += 1
                else:
                    failed += 1
            
            print(f"\n✅ Verification complete: {verified} verified, {failed} failed")
            return failed == 0
            
        except Exception as e:
            print(f"❌ Scheduled verification failed: {str(e)}")
            return False
    
    def create_pre_deploy_backup(self):
        """Create backup before deployment"""
        print(f"\n🚀 Creating pre-deployment backup...")
        try:
            backup_path = self.manager.create_backup('pre-deploy')
            print(f"\n✅ Pre-deployment backup created")
            print(f"   ⚠️  Keep this backup until deployment is verified!")
            return backup_path
        except Exception as e:
            print(f"❌ Pre-deployment backup failed: {str(e)}")
            raise
    
    def run(self):
        """Run scheduler (blocking)"""
        self.schedule_backups()
        self.running = True
        
        print(f"\n▶️  Backup scheduler started!")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print(f"\n⏹️  Backup scheduler stopped")
            self.running = False
    
    def run_once(self):
        """Run all pending tasks once (for testing)"""
        self.schedule_backups()
        
        print(f"\n▶️  Running scheduled tasks once...")
        schedule.run_all()
        print(f"\n✅ All tasks completed")
    
    def status(self):
        """Show scheduler status"""
        print(f"\n📊 Backup Scheduler Status")
        print(f"   Environment: {self.environment}")
        print(f"   Running: {self.running}")
        print(f"\n📅 Scheduled Jobs:")
        
        for job in schedule.get_jobs():
            print(f"   - {job}")


def main():
    """Main scheduler interface"""
    import sys
    
    scheduler = BackupScheduler()
    
    if len(sys.argv) < 2:
        print("\n📚 Backup Scheduler Commands:")
        print("   python backup_scheduler.py start         - Start scheduler (blocking)")
        print("   python backup_scheduler.py once          - Run all jobs once (testing)")
        print("   python backup_scheduler.py status        - Show scheduler status")
        print("   python backup_scheduler.py pre-deploy    - Create pre-deployment backup")
        print("   python backup_scheduler.py backup-now    - Create immediate backup")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        scheduler.run()
        
    elif command == 'once':
        scheduler.run_once()
        
    elif command == 'status':
        scheduler.status()
        
    elif command == 'pre-deploy':
        scheduler.create_pre_deploy_backup()
        
    elif command == 'backup-now':
        scheduler._create_scheduled_backup()
        
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()