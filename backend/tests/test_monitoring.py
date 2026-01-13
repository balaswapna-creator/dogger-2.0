"""
Security Monitoring Test Suite
Week 4 Day 3: Test monitoring and alert systems
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from security_monitor import SecurityMonitor
from log_analyzer import LogAnalyzer
from security_dashboard import SecurityDashboard


class MonitoringTester:
    """Test suite for security monitoring system"""
    
    def __init__(self):
        self.monitor = SecurityMonitor()
        self.analyzer = LogAnalyzer()
        self.dashboard = SecurityDashboard()
        self.test_results = []
        
        print("🧪 Security Monitoring Test Suite")
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
    
    def test_monitor_initialization(self):
        """Test 1: Monitor initialization"""
        print("Testing monitor initialization...")
        
        # Check directories exist
        if not self.monitor.logs_dir.exists():
            print("   ❌ Logs directory missing")
            return False
        
        if not self.monitor.alerts_dir.exists():
            print("   ❌ Alerts directory missing")
            return False
        
        print("   ✓ Monitor initialized")
        print("   ✓ Logs directory exists")
        print("   ✓ Alerts directory exists")
        
        return True
    
    def test_log_parsing(self):
        """Test 2: Log parsing"""
        print("Testing log parsing...")
        
        # Create test log entry
        test_line = "2026-01-10 19:16:58,723 - security - WARNING - Failed login attempt for user: admin from 127.0.0.1"
        
        parsed = self.monitor.parse_log_line(test_line)
        
        if not parsed:
            print("   ❌ Failed to parse log line")
            return False
        
        if 'timestamp' not in parsed:
            print("   ❌ Missing timestamp")
            return False
        
        if 'level' not in parsed:
            print("   ❌ Missing level")
            return False
        
        if 'message' not in parsed:
            print("   ❌ Missing message")
            return False
        
        print("   ✓ Log line parsed successfully")
        print(f"   ✓ Timestamp: {parsed['timestamp']}")
        print(f"   ✓ Level: {parsed['level']}")
        print(f"   ✓ Message: {parsed['message'][:50]}...")
        
        return True
    
    def test_log_analysis(self):
        """Test 3: Log analysis"""
        print("Testing log analysis...")
        
        threats = self.monitor.analyze_logs(24)
        
        if not isinstance(threats, dict):
            print("   ❌ Invalid threats data structure")
            return False
        
        required_keys = [
            'failed_logins',
            'rate_limit_violations',
            'suspicious_requests',
            'sql_injection_attempts',
            'xss_attempts'
        ]
        
        for key in required_keys:
            if key not in threats:
                print(f"   ❌ Missing key: {key}")
                return False
            print(f"   ✓ Found: {key}")
        
        print("   ✓ Log analysis completed")
        
        return True
    
    def test_alert_generation(self):
        """Test 4: Alert generation"""
        print("Testing alert generation...")
        
        test_alert_data = {
            'type': 'TEST_ALERT',
            'severity': 'MEDIUM',
            'message': 'This is a test alert'
        }
        
        alert = self.monitor.generate_alert(test_alert_data)
        
        if not alert:
            print("   ❌ Failed to generate alert")
            return False
        
        if 'id' not in alert:
            print("   ❌ Missing alert ID")
            return False
        
        if 'timestamp' not in alert:
            print("   ❌ Missing timestamp")
            return False
        
        # Check if alert file was created
        alert_file = self.monitor.alerts_dir / f"{alert['id']}.json"
        if not alert_file.exists():
            print("   ❌ Alert file not created")
            return False
        
        print(f"   ✓ Alert generated: {alert['id']}")
        print(f"   ✓ Alert file created")
        print(f"   ✓ Alert saved to history")
        
        return True
    
    def test_security_status(self):
        """Test 5: Security status retrieval"""
        print("Testing security status...")
        
        status = self.monitor.get_security_status()
        
        if not isinstance(status, dict):
            print("   ❌ Invalid status data structure")
            return False
        
        required_fields = [
            'total_alerts',
            'critical',
            'high',
            'medium',
            'security_score'
        ]
        
        for field in required_fields:
            if field not in status:
                print(f"   ❌ Missing field: {field}")
                return False
            print(f"   ✓ {field}: {status[field]}")
        
        if not (0 <= status['security_score'] <= 100):
            print("   ❌ Invalid security score")
            return False
        
        print("   ✓ Security status retrieved")
        
        return True
    
    def test_log_analyzer(self):
        """Test 6: Log analyzer"""
        print("Testing log analyzer...")
        
        # Test security event analysis
        security_analysis = self.analyzer.analyze_security_events(24)
        
        if not isinstance(security_analysis, dict):
            print("   ❌ Invalid analysis data")
            return False
        
        if 'total_events' not in security_analysis:
            print("   ❌ Missing total_events")
            return False
        
        if 'event_breakdown' not in security_analysis:
            print("   ❌ Missing event_breakdown")
            return False
        
        print(f"   ✓ Total events: {security_analysis['total_events']}")
        print("   ✓ Log analyzer working")
        
        return True
    
    def test_daily_report(self):
        """Test 7: Daily report generation"""
        print("Testing daily report generation...")
        
        report = self.analyzer.generate_daily_report()
        
        if not isinstance(report, dict):
            print("   ❌ Invalid report data")
            return False
        
        if 'health_score' not in report:
            print("   ❌ Missing health_score")
            return False
        
        if not (0 <= report['health_score'] <= 100):
            print("   ❌ Invalid health score")
            return False
        
        # Check if report file was created
        report_dir = Path('reports')
        report_files = list(report_dir.glob('daily_report_*.json'))
        
        if not report_files:
            print("   ❌ Report file not created")
            return False
        
        print(f"   ✓ Health score: {report['health_score']}/100")
        print("   ✓ Report generated")
        print("   ✓ Report file created")
        
        return True
    
    def test_dashboard_display(self):
        """Test 8: Dashboard display"""
        print("Testing dashboard display...")
        
        try:
            # This will print the dashboard
            self.dashboard.display_dashboard()
            print("   ✓ Dashboard displayed successfully")
            return True
        except Exception as e:
            print(f"   ❌ Dashboard display failed: {str(e)}")
            return False
    
    def test_html_export(self):
        """Test 9: HTML dashboard export"""
        print("Testing HTML export...")
        
        dashboard_file = self.dashboard.export_dashboard_html()
        
        if not dashboard_file.exists():
            print("   ❌ HTML file not created")
            return False
        
        # Check file size
        file_size = dashboard_file.stat().st_size
        if file_size == 0:
            print("   ❌ HTML file is empty")
            return False
        
        print(f"   ✓ HTML file created: {dashboard_file}")
        print(f"   ✓ File size: {file_size} bytes")
        
        return True
    
    def test_threat_detection(self):
        """Test 10: Threat detection"""
        print("Testing threat detection...")
        
        threats = self.monitor.analyze_logs(24)
        
        # Test brute force detection
        brute_force = self.monitor.detect_brute_force(threats)
        print(f"   ✓ Brute force detector: {len(brute_force)} alerts")
        
        # Test SQL injection detection
        sql_injection = self.monitor.detect_sql_injection(threats)
        print(f"   ✓ SQL injection detector: {len(sql_injection)} alerts")
        
        # Test XSS detection
        xss_attacks = self.monitor.detect_xss_attacks(threats)
        print(f"   ✓ XSS detector: {len(xss_attacks)} alerts")
        
        # Test rate limit detection
        rate_limit = self.monitor.detect_rate_limit_abuse(threats)
        print(f"   ✓ Rate limit detector: {len(rate_limit)} alerts")
        
        # Test suspicious IP detection
        suspicious_ips = self.monitor.detect_suspicious_ips(threats)
        print(f"   ✓ Suspicious IP detector: {len(suspicious_ips)} alerts")
        
        print("   ✓ All threat detectors working")
        
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
            ("Monitor Initialization", self.test_monitor_initialization),
            ("Log Parsing", self.test_log_parsing),
            ("Log Analysis", self.test_log_analysis),
            ("Alert Generation", self.test_alert_generation),
            ("Security Status", self.test_security_status),
            ("Log Analyzer", self.test_log_analyzer),
            ("Daily Report", self.test_daily_report),
            ("Dashboard Display", self.test_dashboard_display),
            ("HTML Export", self.test_html_export),
            ("Threat Detection", self.test_threat_detection),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        return self.print_summary()


def main():
    """Main test interface"""
    tester = MonitoringTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()