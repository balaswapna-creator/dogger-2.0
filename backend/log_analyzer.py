"""
Advanced Log Analysis Tool
Week 4 Day 3: Analyze and visualize security logs
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
import json

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()


class LogAnalyzer:
    """Analyze security and application logs"""
    
    def __init__(self):
        self.logs_dir = Path('logs')
        self.reports_dir = Path('reports')
        self.reports_dir.mkdir(exist_ok=True)
        
        # Available log files
        self.log_files = {
            'security': self.logs_dir / 'security.log',
            'application': self.logs_dir / 'dogger.log',
            'errors': self.logs_dir / 'errors.log',
        }
        
        print("📊 Log Analyzer initialized")
        print(f"   Logs directory: {self.logs_dir}")
        print(f"   Reports directory: {self.reports_dir}")
    
    def parse_log_file(self, log_type='security', hours=24):
        """Parse log file and extract events"""
        log_file = self.log_files.get(log_type)
        
        if not log_file or not log_file.exists():
            print(f"⚠️  Log file not found: {log_type}")
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        events = []
        
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                try:
                    # Parse timestamp
                    parts = line.split(' - ')
                    if len(parts) < 4:
                        continue
                    
                    timestamp_str = parts[0].strip()
                    log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                    
                    if log_time < cutoff_time:
                        continue
                    
                    event = {
                        'timestamp': timestamp_str,
                        'datetime': log_time,
                        'logger': parts[1].strip(),
                        'level': parts[2].strip(),
                        'message': ' - '.join(parts[3:]).strip()
                    }
                    events.append(event)
                    
                except Exception as e:
                    continue
        
        return events
    
    def analyze_error_patterns(self, hours=24):
        """Analyze error patterns"""
        print(f"\n🔍 Analyzing error patterns (last {hours} hours)...")
        
        events = self.parse_log_file('errors', hours)
        
        if not events:
            print("   ✅ No errors found")
            return {}
        
        # Group errors
        error_types = Counter()
        error_details = defaultdict(list)
        
        for event in events:
            # Extract error type
            message = event['message']
            
            # Common error patterns
            if 'exception' in message.lower():
                error_type = 'Exception'
            elif 'traceback' in message.lower():
                error_type = 'Traceback'
            elif 'error' in message.lower():
                error_type = 'Error'
            else:
                error_type = 'Unknown'
            
            error_types[error_type] += 1
            error_details[error_type].append(event)
        
        print(f"\n📊 Error Summary:")
        print(f"   Total Errors: {len(events)}")
        for error_type, count in error_types.most_common():
            print(f"   {error_type}: {count}")
        
        return {
            'total_errors': len(events),
            'error_types': dict(error_types),
            'details': error_details
        }
    
    def analyze_request_patterns(self, hours=24):
        """Analyze request patterns"""
        print(f"\n🌐 Analyzing request patterns (last {hours} hours)...")
        
        events = self.parse_log_file('application', hours)
        
        if not events:
            print("   ℹ️  No application logs found")
            return {}
        
        # Extract IPs and endpoints
        ip_requests = Counter()
        endpoints = Counter()
        hourly_requests = defaultdict(int)
        
        for event in events:
            message = event['message']
            
            # Extract IP
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', message)
            if ip_match:
                ip_requests[ip_match.group(1)] += 1
            
            # Extract endpoint
            endpoint_match = re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+(/\S+)', message)
            if endpoint_match:
                endpoints[endpoint_match.group(2)] += 1
            
            # Group by hour
            hour = event['datetime'].strftime('%Y-%m-%d %H:00')
            hourly_requests[hour] += 1
        
        print(f"\n📊 Request Summary:")
        print(f"   Total Requests: {len(events)}")
        print(f"   Unique IPs: {len(ip_requests)}")
        print(f"   Unique Endpoints: {len(endpoints)}")
        
        print(f"\n🔝 Top IPs:")
        for ip, count in ip_requests.most_common(5):
            print(f"   {ip}: {count} requests")
        
        print(f"\n🔝 Top Endpoints:")
        for endpoint, count in endpoints.most_common(5):
            print(f"   {endpoint}: {count} requests")
        
        return {
            'total_requests': len(events),
            'unique_ips': len(ip_requests),
            'unique_endpoints': len(endpoints),
            'top_ips': dict(ip_requests.most_common(10)),
            'top_endpoints': dict(endpoints.most_common(10)),
            'hourly_distribution': dict(hourly_requests)
        }
    
    def analyze_security_events(self, hours=24):
        """Analyze security events"""
        print(f"\n🔒 Analyzing security events (last {hours} hours)...")
        
        events = self.parse_log_file('security', hours)
        
        if not events:
            print("   ✅ No security events")
            return {}
        
        # Categorize events
        event_types = {
            'login_success': [],
            'login_failed': [],
            'logout': [],
            'rate_limited': [],
            'blocked': [],
            'suspicious': [],
            'other': []
        }
        
        for event in events:
            message = event['message'].lower()
            
            if 'successful login' in message or 'login successful' in message:
                event_types['login_success'].append(event)
            elif 'failed login' in message or 'login failed' in message:
                event_types['login_failed'].append(event)
            elif 'logout' in message:
                event_types['logout'].append(event)
            elif 'rate limit' in message:
                event_types['rate_limited'].append(event)
            elif 'blocked' in message:
                event_types['blocked'].append(event)
            elif 'suspicious' in message or 'attack' in message:
                event_types['suspicious'].append(event)
            else:
                event_types['other'].append(event)
        
        print(f"\n📊 Security Event Summary:")
        print(f"   Total Events: {len(events)}")
        print(f"   ✅ Successful Logins: {len(event_types['login_success'])}")
        print(f"   ❌ Failed Logins: {len(event_types['login_failed'])}")
        print(f"   🚪 Logouts: {len(event_types['logout'])}")
        print(f"   ⏱️  Rate Limited: {len(event_types['rate_limited'])}")
        print(f"   🚫 Blocked: {len(event_types['blocked'])}")
        print(f"   ⚠️  Suspicious: {len(event_types['suspicious'])}")
        
        return {
            'total_events': len(events),
            'event_breakdown': {k: len(v) for k, v in event_types.items()},
            'details': event_types
        }
    
    def generate_daily_report(self):
        """Generate comprehensive daily report"""
        print("\n" + "=" * 60)
        print("📈 DAILY SECURITY REPORT")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Period: Last 24 hours")
        
        # Analyze all aspects
        security_analysis = self.analyze_security_events(24)
        request_analysis = self.analyze_request_patterns(24)
        error_analysis = self.analyze_error_patterns(24)
        
        # Compile report
        report = {
            'generated_at': datetime.now().isoformat(),
            'period_hours': 24,
            'security_events': security_analysis,
            'request_patterns': request_analysis,
            'error_patterns': error_analysis,
        }
        
        # Calculate health score
        health_score = 100
        
        # Deduct for errors
        if error_analysis.get('total_errors', 0) > 0:
            health_score -= min(20, error_analysis['total_errors'] * 2)
        
        # Deduct for failed logins
        failed_logins = security_analysis.get('event_breakdown', {}).get('login_failed', 0)
        if failed_logins > 5:
            health_score -= min(15, (failed_logins - 5) * 3)
        
        # Deduct for suspicious activity
        suspicious = security_analysis.get('event_breakdown', {}).get('suspicious', 0)
        if suspicious > 0:
            health_score -= min(25, suspicious * 5)
        
        health_score = max(0, health_score)
        report['health_score'] = health_score
        
        print("\n" + "=" * 60)
        print("🎯 SYSTEM HEALTH")
        print("=" * 60)
        print(f"Health Score: {health_score}/100")
        
        if health_score >= 90:
            print("Status: ✅ Excellent")
        elif health_score >= 70:
            print("Status: ⚠️  Good with minor issues")
        elif health_score >= 50:
            print("Status: ⚠️  Needs attention")
        else:
            print("Status: 🚨 Critical issues detected")
        
        # Save report
        report_file = self.reports_dir / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📄 Report saved: {report_file}")
        print("=" * 60)
        
        return report
    
    def analyze_trends(self, days=7):
        """Analyze trends over multiple days"""
        print(f"\n📈 Analyzing trends (last {days} days)...")
        
        trends = {
            'daily_errors': [],
            'daily_failed_logins': [],
            'daily_requests': [],
        }
        
        for day in range(days):
            hours_ago = day * 24
            
            # Get data for this day
            errors = self.parse_log_file('errors', hours=24)
            security = self.parse_log_file('security', hours=24)
            requests = self.parse_log_file('application', hours=24)
            
            # Count failed logins
            failed_logins = sum(1 for e in security if 'failed login' in e['message'].lower())
            
            trends['daily_errors'].append(len(errors))
            trends['daily_failed_logins'].append(failed_logins)
            trends['daily_requests'].append(len(requests))
        
        print(f"\n📊 Trend Summary:")
        print(f"   Avg Daily Errors: {sum(trends['daily_errors']) / len(trends['daily_errors']):.1f}")
        print(f"   Avg Failed Logins: {sum(trends['daily_failed_logins']) / len(trends['daily_failed_logins']):.1f}")
        print(f"   Avg Daily Requests: {sum(trends['daily_requests']) / len(trends['daily_requests']):.1f}")
        
        return trends
    
    def search_logs(self, pattern, log_type='all', hours=24):
        """Search logs for specific pattern"""
        print(f"\n🔍 Searching for pattern: '{pattern}'")
        
        results = []
        log_types = list(self.log_files.keys()) if log_type == 'all' else [log_type]
        
        for lt in log_types:
            events = self.parse_log_file(lt, hours)
            matches = [e for e in events if re.search(pattern, e['message'], re.IGNORECASE)]
            
            if matches:
                print(f"\n📄 Found {len(matches)} match(es) in {lt} log:")
                for match in matches[:10]:  # Show first 10
                    print(f"   [{match['timestamp']}] {match['message'][:80]}...")
                
                results.extend(matches)
        
        print(f"\n✅ Total matches: {len(results)}")
        return results


def main():
    """Main log analyzer interface"""
    import sys
    
    analyzer = LogAnalyzer()
    
    if len(sys.argv) < 2:
        print("\n📚 Log Analyzer Commands:")
        print("   python log_analyzer.py daily-report        - Generate daily report")
        print("   python log_analyzer.py security [hours]    - Analyze security events")
        print("   python log_analyzer.py errors [hours]      - Analyze errors")
        print("   python log_analyzer.py requests [hours]    - Analyze requests")
        print("   python log_analyzer.py trends [days]       - Analyze trends")
        print("   python log_analyzer.py search <pattern>    - Search logs")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'daily-report':
        analyzer.generate_daily_report()
    
    elif command == 'security':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        analyzer.analyze_security_events(hours)
    
    elif command == 'errors':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        analyzer.analyze_error_patterns(hours)
    
    elif command == 'requests':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        analyzer.analyze_request_patterns(hours)
    
    elif command == 'trends':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        analyzer.analyze_trends(days)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("❌ Error: Please provide search pattern")
            return
        pattern = sys.argv[2]
        analyzer.search_logs(pattern)
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()