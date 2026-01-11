"""
Real-time Security Dashboard
Week 4 Day 3: Visual security monitoring dashboard
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from security_monitor import SecurityMonitor
from log_analyzer import LogAnalyzer


class SecurityDashboard:
    """Real-time security dashboard"""
    
    def __init__(self):
        self.monitor = SecurityMonitor()
        self.analyzer = LogAnalyzer()
        
        print("🎛️  Security Dashboard initialized")
    
    def display_dashboard(self):
        """Display comprehensive security dashboard"""
        
        # Clear screen (works on Windows and Unix)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("🔒 DOGGER 2.0 SECURITY DASHBOARD")
        print("=" * 80)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Security Status
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 🎯 SECURITY STATUS                                                          │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        status = self.monitor.get_security_status()
        
        # Security Score with color
        score = status['security_score']
        if score >= 90:
            score_status = f"✅ {score}/100 - EXCELLENT"
        elif score >= 70:
            score_status = f"⚠️  {score}/100 - GOOD"
        elif score >= 50:
            score_status = f"⚠️  {score}/100 - NEEDS ATTENTION"
        else:
            score_status = f"🚨 {score}/100 - CRITICAL"
        
        print(f"\n   Security Score: {score_status}")
        
        # Alert Summary
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 🚨 ALERT SUMMARY (Last 7 Days)                                              │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        print(f"\n   Total Alerts: {status['total_alerts']}")
        print(f"   🔴 Critical: {status['critical']}")
        print(f"   🟡 High: {status['high']}")
        print(f"   🟢 Medium: {status['medium']}")
        
        # Security Events (Last 24h)
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 📊 SECURITY EVENTS (Last 24 Hours)                                          │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        security_events = self.analyzer.analyze_security_events(24)
        breakdown = security_events.get('event_breakdown', {})
        
        print(f"\n   Total Events: {security_events.get('total_events', 0)}")
        print(f"   ✅ Successful Logins: {breakdown.get('login_success', 0)}")
        print(f"   ❌ Failed Logins: {breakdown.get('login_failed', 0)}")
        print(f"   🚪 Logouts: {breakdown.get('logout', 0)}")
        print(f"   ⏱️  Rate Limited: {breakdown.get('rate_limited', 0)}")
        print(f"   🚫 Blocked: {breakdown.get('blocked', 0)}")
        print(f"   ⚠️  Suspicious: {breakdown.get('suspicious', 0)}")
        
        # Error Analysis
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 🐛 ERROR ANALYSIS (Last 24 Hours)                                           │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        errors = self.analyzer.analyze_error_patterns(24)
        
        if errors.get('total_errors', 0) == 0:
            print("\n   ✅ No errors detected")
        else:
            print(f"\n   Total Errors: {errors.get('total_errors', 0)}")
            error_types = errors.get('error_types', {})
            for error_type, count in list(error_types.items())[:5]:
                print(f"   • {error_type}: {count}")
        
        # Request Patterns
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 🌐 REQUEST PATTERNS (Last 24 Hours)                                         │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        requests = self.analyzer.analyze_request_patterns(24)
        
        print(f"\n   Total Requests: {requests.get('total_requests', 0)}")
        print(f"   Unique IPs: {requests.get('unique_ips', 0)}")
        print(f"   Unique Endpoints: {requests.get('unique_endpoints', 0)}")
        
        # Top IPs
        top_ips = requests.get('top_ips', {})
        if top_ips:
            print("\n   Top IPs:")
            for ip, count in list(top_ips.items())[:3]:
                print(f"   • {ip}: {count} requests")
        
        # Recent Alerts
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 📋 RECENT ALERTS (Last 5)                                                   │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        recent_alerts = self.monitor.alert_history[-5:]
        recent_alerts.reverse()
        
        if not recent_alerts:
            print("\n   ✅ No recent alerts")
        else:
            for alert in recent_alerts:
                severity_icon = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟡',
                    'MEDIUM': '🟢'
                }.get(alert.get('severity'), '⚪')
                
                print(f"\n   {severity_icon} [{alert.get('datetime', 'N/A')}]")
                print(f"   {alert.get('type', 'Unknown')}")
                print(f"   {alert.get('message', 'No message')[:70]}...")
        
        # System Recommendations
        print("\n┌─────────────────────────────────────────────────────────────────────────────┐")
        print("│ 💡 RECOMMENDATIONS                                                          │")
        print("└─────────────────────────────────────────────────────────────────────────────┘")
        
        recommendations = []
        
        if breakdown.get('login_failed', 0) > 10:
            recommendations.append("⚠️  High number of failed logins - consider implementing CAPTCHA")
        
        if breakdown.get('rate_limited', 0) > 20:
            recommendations.append("⚠️  Many rate limit violations - review rate limiting thresholds")
        
        if breakdown.get('suspicious', 0) > 0:
            recommendations.append("🚨 Suspicious activity detected - review security logs immediately")
        
        if errors.get('total_errors', 0) > 50:
            recommendations.append("⚠️  High error rate - investigate application issues")
        
        if score < 70:
            recommendations.append("🚨 Security score is low - run full security audit")
        
        if not recommendations:
            recommendations.append("✅ No immediate actions required - system is healthy")
        
        for rec in recommendations:
            print(f"\n   {rec}")
        
        # Footer
        print("\n" + "=" * 80)
        print("Commands:")
        print("  python security_monitor.py scan     - Run security scan")
        print("  python log_analyzer.py daily-report - Generate daily report")
        print("  python security_dashboard.py        - Refresh dashboard")
        print("=" * 80)
    
    def display_live_dashboard(self, refresh_seconds=60):
        """Display live updating dashboard"""
        import time
        
        print("🎛️  Starting live dashboard (Press Ctrl+C to stop)...")
        print(f"Refresh interval: {refresh_seconds} seconds\n")
        
        try:
            while True:
                self.display_dashboard()
                print(f"\n⏰ Auto-refresh in {refresh_seconds} seconds...")
                time.sleep(refresh_seconds)
        except KeyboardInterrupt:
            print("\n\n✋ Dashboard stopped")
    
    def export_dashboard_html(self):
        """Export dashboard as HTML report"""
        print("📄 Generating HTML dashboard...")
        
        # Get all data
        status = self.monitor.get_security_status()
        security_events = self.analyzer.analyze_security_events(24)
        errors = self.analyzer.analyze_error_patterns(24)
        requests = self.analyzer.analyze_request_patterns(24)
        
        # Generate HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Dogger 2.0 Security Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .metric-card.critical {{
            border-left-color: #e74c3c;
        }}
        .metric-card.warning {{
            border-left-color: #f39c12;
        }}
        .metric-card.success {{
            border-left-color: #2ecc71;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .alert {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }}
        .alert-critical {{
            background: #fee;
            border-left-color: #e74c3c;
        }}
        .alert-warning {{
            background: #fef9e7;
            border-left-color: #f39c12;
        }}
        .timestamp {{
            color: #95a5a6;
            font-size: 0.9em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #3498db;
            color: white;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Dogger 2.0 Security Dashboard</h1>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metric-grid">
            <div class="metric-card {'success' if status['security_score'] >= 90 else 'warning' if status['security_score'] >= 70 else 'critical'}">
                <div class="metric-value">{status['security_score']}/100</div>
                <div class="metric-label">Security Score</div>
            </div>
            <div class="metric-card {'critical' if status['critical'] > 0 else 'success'}">
                <div class="metric-value">{status['critical']}</div>
                <div class="metric-label">Critical Alerts</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{security_events.get('total_events', 0)}</div>
                <div class="metric-label">Security Events (24h)</div>
            </div>
            <div class="metric-card {'critical' if errors.get('total_errors', 0) > 50 else 'success'}">
                <div class="metric-value">{errors.get('total_errors', 0)}</div>
                <div class="metric-label">Errors (24h)</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Security Events (Last 24 Hours)</h2>
            <table>
                <tr>
                    <th>Event Type</th>
                    <th>Count</th>
                </tr>
                <tr><td>✅ Successful Logins</td><td>{security_events.get('event_breakdown', {}).get('login_success', 0)}</td></tr>
                <tr><td>❌ Failed Logins</td><td>{security_events.get('event_breakdown', {}).get('login_failed', 0)}</td></tr>
                <tr><td>🚪 Logouts</td><td>{security_events.get('event_breakdown', {}).get('logout', 0)}</td></tr>
                <tr><td>⏱️ Rate Limited</td><td>{security_events.get('event_breakdown', {}).get('rate_limited', 0)}</td></tr>
                <tr><td>⚠️ Suspicious</td><td>{security_events.get('event_breakdown', {}).get('suspicious', 0)}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>🌐 Request Statistics (Last 24 Hours)</h2>
            <p>Total Requests: <strong>{requests.get('total_requests', 0)}</strong></p>
            <p>Unique IPs: <strong>{requests.get('unique_ips', 0)}</strong></p>
            <p>Unique Endpoints: <strong>{requests.get('unique_endpoints', 0)}</strong></p>
        </div>
        
        <div class="section">
            <h2>🚨 Recent Alerts</h2>
            {''.join([f'<div class="alert alert-{alert.get("severity", "warning").lower()}">' +
                     f'<strong>{alert.get("type", "Unknown")}</strong><br>' +
                     f'{alert.get("message", "No message")}<br>' +
                     f'<span class="timestamp">{alert.get("datetime", "N/A")}</span></div>' 
                     for alert in self.monitor.alert_history[-5:]][::-1]) if self.monitor.alert_history else '<p>No recent alerts</p>'}
        </div>
        
        <div class="section">
            <p class="timestamp">Dashboard auto-updates every 5 minutes. Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML
        dashboard_file = Path('reports') / f"security_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        dashboard_file.parent.mkdir(exist_ok=True)
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Dashboard exported: {dashboard_file}")
        print(f"   Open in browser to view")
        
        return dashboard_file


def main():
    """Main dashboard interface"""
    import sys
    
    dashboard = SecurityDashboard()
    
    if len(sys.argv) < 2:
        # Default: show dashboard once
        dashboard.display_dashboard()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'live':
        refresh = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        dashboard.display_live_dashboard(refresh)
    
    elif command == 'export':
        dashboard.export_dashboard_html()
    
    else:
        dashboard.display_dashboard()


if __name__ == '__main__':
    main()