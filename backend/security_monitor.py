"""
Real-time Security Monitoring System
Week 4 Day 3: Monitor security events and detect threats
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from clinic.config import config


class SecurityMonitor:
    """Real-time security event monitoring and alerting"""
    
    def __init__(self):
        self.logs_dir = Path('logs')
        self.security_log = self.logs_dir / 'security.log'
        self.alerts_dir = Path('alerts')
        self.alerts_dir.mkdir(exist_ok=True)
        
        # Threat thresholds
        self.thresholds = {
            'failed_login_attempts': 5,      # 5 failed logins = alert
            'rate_limit_violations': 10,     # 10 rate limit hits = alert
            'suspicious_requests': 20,       # 20 suspicious requests = alert
            'sql_injection_attempts': 1,     # Any SQL injection = immediate alert
            'xss_attempts': 1,               # Any XSS attempt = immediate alert
            'brute_force_window': 300,       # 5 minutes window for brute force
        }
        
        # Alert history
        self.alert_history = []
        self.load_alert_history()
        
        print("🔒 Security Monitor initialized")
        print(f"   Monitoring: {self.security_log}")
        print(f"   Alerts dir: {self.alerts_dir}")
    
    def load_alert_history(self):
        """Load previous alerts"""
        history_file = self.alerts_dir / 'alert_history.json'
        if history_file.exists():
            with open(history_file, 'r') as f:
                self.alert_history = json.load(f)
    
    def save_alert_history(self):
        """Save alert history"""
        history_file = self.alerts_dir / 'alert_history.json'
        with open(history_file, 'w') as f:
            json.dump(self.alert_history, f, indent=2)
    
    def parse_log_line(self, line):
        """Parse security log line"""
        try:
            # Example: 2026-01-10 19:16:58,723 - security - WARNING - Failed login attempt for user: admin from 127.0.0.1
            parts = line.split(' - ')
            if len(parts) >= 4:
                timestamp = parts[0].strip()
                level = parts[2].strip()
                message = ' - '.join(parts[3:]).strip()
                
                return {
                    'timestamp': timestamp,
                    'level': level,
                    'message': message,
                    'raw': line
                }
        except Exception as e:
            return None
        
        return None
    
    def analyze_logs(self, hours=24):
        """Analyze security logs for threats"""
        if not self.security_log.exists():
            print("⚠️  No security log found")
            return {}
        
        print(f"\n🔍 Analyzing security logs (last {hours} hours)...")
        
        # Calculate time window
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Threat counters
        threats = {
            'failed_logins': [],
            'rate_limit_violations': [],
            'suspicious_requests': [],
            'sql_injection_attempts': [],
            'xss_attempts': [],
            'blocked_ips': Counter(),
            'user_login_attempts': defaultdict(list),
            'ip_requests': defaultdict(list),
        }
        
        # Parse logs
        with open(self.security_log, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = self.parse_log_line(line)
                if not parsed:
                    continue
                
                try:
                    # Parse timestamp
                    log_time = datetime.strptime(parsed['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
                    
                    # Only analyze recent logs
                    if log_time < cutoff_time:
                        continue
                    
                except Exception:
                    continue
                
                message = parsed['message'].lower()
                
                # Detect failed logins
                if 'failed login' in message:
                    threats['failed_logins'].append(parsed)
                    # Extract username and IP
                    user_match = re.search(r'user:?\s*(\w+)', message)
                    ip_match = re.search(r'from\s+([\d.]+)', message)
                    if user_match:
                        username = user_match.group(1)
                        threats['user_login_attempts'][username].append(parsed)
                
                # Detect rate limiting
                if 'rate limit' in message or 'too many requests' in message:
                    threats['rate_limit_violations'].append(parsed)
                
                # Detect SQL injection attempts
                sql_keywords = ['union', 'select', 'drop', 'insert', 'delete', '--', 'or 1=1']
                if any(keyword in message for keyword in sql_keywords):
                    if 'sql' in message or 'injection' in message:
                        threats['sql_injection_attempts'].append(parsed)
                
                # Detect XSS attempts
                xss_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=']
                if any(pattern in message for pattern in xss_patterns):
                    threats['xss_attempts'].append(parsed)
                
                # Track IP addresses
                ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', message)
                if ip_match:
                    ip = ip_match.group(1)
                    threats['ip_requests'][ip].append(parsed)
        
        return threats
    
    def detect_brute_force(self, threats):
        """Detect brute force attacks"""
        print("\n🔨 Checking for brute force attacks...")
        
        brute_force_alerts = []
        
        for username, attempts in threats['user_login_attempts'].items():
            if len(attempts) >= self.thresholds['failed_login_attempts']:
                # Check if within time window
                recent_attempts = []
                now = datetime.now()
                
                for attempt in attempts:
                    try:
                        attempt_time = datetime.strptime(attempt['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
                        if (now - attempt_time).total_seconds() <= self.thresholds['brute_force_window']:
                            recent_attempts.append(attempt)
                    except:
                        continue
                
                if len(recent_attempts) >= self.thresholds['failed_login_attempts']:
                    alert = {
                        'type': 'BRUTE_FORCE_ATTACK',
                        'severity': 'CRITICAL',
                        'username': username,
                        'attempts': len(recent_attempts),
                        'window': f"{self.thresholds['brute_force_window']}s",
                        'first_attempt': recent_attempts[0]['timestamp'],
                        'last_attempt': recent_attempts[-1]['timestamp'],
                        'message': f"Brute force attack detected on user '{username}': {len(recent_attempts)} failed login attempts in {self.thresholds['brute_force_window']} seconds"
                    }
                    brute_force_alerts.append(alert)
                    print(f"   ⚠️  {alert['message']}")
        
        return brute_force_alerts
    
    def detect_sql_injection(self, threats):
        """Detect SQL injection attempts"""
        print("\n💉 Checking for SQL injection attempts...")
        
        sql_alerts = []
        
        if len(threats['sql_injection_attempts']) >= self.thresholds['sql_injection_attempts']:
            alert = {
                'type': 'SQL_INJECTION_ATTEMPT',
                'severity': 'CRITICAL',
                'attempts': len(threats['sql_injection_attempts']),
                'message': f"SQL injection attempts detected: {len(threats['sql_injection_attempts'])} attempts",
                'samples': [a['message'] for a in threats['sql_injection_attempts'][:3]]
            }
            sql_alerts.append(alert)
            print(f"   🚨 {alert['message']}")
        
        return sql_alerts
    
    def detect_xss_attacks(self, threats):
        """Detect XSS attack attempts"""
        print("\n🕷️  Checking for XSS attacks...")
        
        xss_alerts = []
        
        if len(threats['xss_attempts']) >= self.thresholds['xss_attempts']:
            alert = {
                'type': 'XSS_ATTACK_ATTEMPT',
                'severity': 'HIGH',
                'attempts': len(threats['xss_attempts']),
                'message': f"XSS attack attempts detected: {len(threats['xss_attempts'])} attempts",
                'samples': [a['message'] for a in threats['xss_attempts'][:3]]
            }
            xss_alerts.append(alert)
            print(f"   ⚠️  {alert['message']}")
        
        return xss_alerts
    
    def detect_rate_limit_abuse(self, threats):
        """Detect rate limit violations"""
        print("\n⏱️  Checking for rate limit abuse...")
        
        rate_limit_alerts = []
        
        if len(threats['rate_limit_violations']) >= self.thresholds['rate_limit_violations']:
            # Group by IP
            ip_violations = defaultdict(int)
            for violation in threats['rate_limit_violations']:
                ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', violation['message'])
                if ip_match:
                    ip_violations[ip_match.group(1)] += 1
            
            for ip, count in ip_violations.items():
                if count >= self.thresholds['rate_limit_violations']:
                    alert = {
                        'type': 'RATE_LIMIT_ABUSE',
                        'severity': 'MEDIUM',
                        'ip': ip,
                        'violations': count,
                        'message': f"Rate limit abuse from {ip}: {count} violations"
                    }
                    rate_limit_alerts.append(alert)
                    print(f"   ⚠️  {alert['message']}")
        
        return rate_limit_alerts
    
    def detect_suspicious_ips(self, threats):
        """Detect suspicious IP behavior"""
        print("\n🌐 Checking for suspicious IP addresses...")
        
        suspicious_ip_alerts = []
        
        for ip, requests in threats['ip_requests'].items():
            if len(requests) >= self.thresholds['suspicious_requests']:
                alert = {
                    'type': 'SUSPICIOUS_IP_ACTIVITY',
                    'severity': 'MEDIUM',
                    'ip': ip,
                    'requests': len(requests),
                    'message': f"Suspicious activity from {ip}: {len(requests)} requests"
                }
                suspicious_ip_alerts.append(alert)
                print(f"   ⚠️  {alert['message']}")
        
        return suspicious_ip_alerts
    
    def generate_alert(self, alert_data):
        """Generate and save security alert"""
        timestamp = datetime.now().isoformat()
        
        alert = {
            'id': f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': timestamp,
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **alert_data
        }
        
        # Save individual alert
        alert_file = self.alerts_dir / f"{alert['id']}.json"
        with open(alert_file, 'w') as f:
            json.dump(alert, f, indent=2)
        
        # Add to history
        self.alert_history.append(alert)
        self.save_alert_history()
        
        return alert
    
    def send_alert_email(self, alert):
        """Send alert via email (if configured)"""
        # Email settings from environment
        email_enabled = config.get('ALERT_EMAIL_ENABLED', 'false').lower() == 'true'
        
        if not email_enabled:
            print(f"   📧 Email alerts disabled (configure in .env)")
            return False
        
        # This is a placeholder - configure with real SMTP settings
        print(f"   📧 Email alert would be sent for: {alert['type']}")
        return True
    
    def run_security_scan(self, hours=24):
        """Run complete security scan"""
        print("\n" + "=" * 60)
        print("🔒 SECURITY SCAN")
        print("=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Scanning last {hours} hours")
        
        # Analyze logs
        threats = self.analyze_logs(hours)
        
        # Detect threats
        all_alerts = []
        all_alerts.extend(self.detect_brute_force(threats))
        all_alerts.extend(self.detect_sql_injection(threats))
        all_alerts.extend(self.detect_xss_attacks(threats))
        all_alerts.extend(self.detect_rate_limit_abuse(threats))
        all_alerts.extend(self.detect_suspicious_ips(threats))
        
        # Generate alerts
        print("\n" + "=" * 60)
        print("📊 SCAN RESULTS")
        print("=" * 60)
        
        if all_alerts:
            print(f"\n🚨 {len(all_alerts)} SECURITY ALERT(S) DETECTED!\n")
            
            for alert_data in all_alerts:
                alert = self.generate_alert(alert_data)
                print(f"Alert ID: {alert['id']}")
                print(f"Severity: {alert['severity']}")
                print(f"Type: {alert['type']}")
                print(f"Message: {alert['message']}")
                print("-" * 60)
                
                # Send email notification
                self.send_alert_email(alert)
        else:
            print("\n✅ No security threats detected")
        
        # Summary
        print("\n" + "=" * 60)
        print("📈 THREAT SUMMARY")
        print("=" * 60)
        print(f"Failed Login Attempts: {len(threats['failed_logins'])}")
        print(f"Rate Limit Violations: {len(threats['rate_limit_violations'])}")
        print(f"SQL Injection Attempts: {len(threats['sql_injection_attempts'])}")
        print(f"XSS Attempts: {len(threats['xss_attempts'])}")
        print(f"Suspicious IPs: {len([ip for ip, reqs in threats['ip_requests'].items() if len(reqs) >= 10])}")
        print(f"Total Alerts Generated: {len(all_alerts)}")
        print("=" * 60)
        
        return all_alerts
    
    def get_security_status(self):
        """Get current security status"""
        print("\n" + "=" * 60)
        print("📊 SECURITY STATUS")
        print("=" * 60)
        
        # Recent alerts
        recent_alerts = [a for a in self.alert_history if 
                        datetime.fromisoformat(a['timestamp']) > datetime.now() - timedelta(days=7)]
        
        critical_alerts = [a for a in recent_alerts if a['severity'] == 'CRITICAL']
        high_alerts = [a for a in recent_alerts if a['severity'] == 'HIGH']
        medium_alerts = [a for a in recent_alerts if a['severity'] == 'MEDIUM']
        
        print(f"\nAlerts (Last 7 Days): {len(recent_alerts)}")
        print(f"  🔴 Critical: {len(critical_alerts)}")
        print(f"  🟡 High: {len(high_alerts)}")
        print(f"  🟢 Medium: {len(medium_alerts)}")
        
        # Security score
        score = 100
        score -= len(critical_alerts) * 10
        score -= len(high_alerts) * 5
        score -= len(medium_alerts) * 2
        score = max(0, score)
        
        print(f"\n🎯 Security Score: {score}/100")
        
        if score >= 90:
            print("   ✅ Excellent security posture")
        elif score >= 70:
            print("   ⚠️  Good, but needs attention")
        else:
            print("   🚨 Critical security issues detected")
        
        print("=" * 60)
        
        return {
            'total_alerts': len(recent_alerts),
            'critical': len(critical_alerts),
            'high': len(high_alerts),
            'medium': len(medium_alerts),
            'security_score': score
        }
    
    def list_alerts(self, severity=None, limit=10):
        """List recent alerts"""
        print("\n" + "=" * 60)
        print("📋 RECENT ALERTS")
        print("=" * 60)
        
        alerts = self.alert_history[-limit:]
        alerts.reverse()
        
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity.upper()]
        
        if not alerts:
            print("\n✅ No alerts found")
            return []
        
        for alert in alerts:
            print(f"\nAlert ID: {alert['id']}")
            print(f"Time: {alert['datetime']}")
            print(f"Severity: {alert['severity']}")
            print(f"Type: {alert['type']}")
            print(f"Message: {alert['message']}")
            print("-" * 60)
        
        return alerts


def main():
    """Main security monitor interface"""
    import sys
    
    monitor = SecurityMonitor()
    
    if len(sys.argv) < 2:
        print("\n📚 Security Monitor Commands:")
        print("   python security_monitor.py scan [hours]     - Run security scan (default: 24h)")
        print("   python security_monitor.py status           - Show security status")
        print("   python security_monitor.py alerts [limit]   - List recent alerts")
        print("   python security_monitor.py critical         - List critical alerts only")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'scan':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        monitor.run_security_scan(hours)
    
    elif command == 'status':
        monitor.get_security_status()
    
    elif command == 'alerts':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        monitor.list_alerts(limit=limit)
    
    elif command == 'critical':
        monitor.list_alerts(severity='CRITICAL')
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()