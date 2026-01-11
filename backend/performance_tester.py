"""
Performance Testing System for Dogger 2.0
Tests load, stress, and benchmark performance
"""

import time
import requests
import statistics
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))


class PerformanceTester:
    """Comprehensive performance testing system"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.results = []
        self.auth_token = None
        
    def authenticate(self, username: str = "admin", password: str = "admin123") -> bool:
        """Authenticate and get access token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/token/",
                json={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                self.auth_token = response.json().get('access')
                print("✅ Authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    def measure_endpoint(self, method: str, endpoint: str, data: Dict = None, 
                         authenticated: bool = False) -> Tuple[float, int, str]:
        """
        Measure single endpoint request
        Returns: (response_time, status_code, error_message)
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Add auth header if needed
        if authenticated and self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return 0.0, 0, f"Unsupported method: {method}"
            
            response_time = time.time() - start_time
            
            # If 401, try to re-authenticate once
            if response.status_code == 401 and authenticated:
                if self.authenticate():
                    headers["Authorization"] = f"Bearer {self.auth_token}"
                    # Retry request
                    if method.upper() == "GET":
                        response = requests.get(url, headers=headers, timeout=10)
                    response_time = time.time() - start_time
            
            return response_time, response.status_code, ""
            
        except requests.exceptions.Timeout:
            return time.time() - start_time, 0, "Timeout"
        except requests.exceptions.ConnectionError:
            return time.time() - start_time, 0, "Connection Error"
        except Exception as e:
            return time.time() - start_time, 0, str(e)
    
    def load_test(self, endpoint: str, num_requests: int = 100, 
                  concurrent_users: int = 10, authenticated: bool = False) -> Dict:
        """
        Load test: Simulate multiple concurrent users
        """
        print(f"\n{'='*60}")
        print(f"🔄 LOAD TEST: {endpoint}")
        print(f"{'='*60}")
        print(f"Requests: {num_requests} | Concurrent Users: {concurrent_users}")
        
        results = []
        errors = []
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [
                executor.submit(self.measure_endpoint, "GET", endpoint, None, authenticated)
                for _ in range(num_requests)
            ]
            
            for i, future in enumerate(as_completed(futures), 1):
                response_time, status_code, error = future.result()
                
                if status_code == 200:
                    results.append(response_time)
                    if i % 10 == 0:
                        print(f"  ✓ {i}/{num_requests} requests completed")
                else:
                    errors.append({"status": status_code, "error": error})
        
        total_time = time.time() - start_time
        
        # Calculate statistics
        if results:
            stats = {
                "endpoint": endpoint,
                "total_requests": num_requests,
                "concurrent_users": concurrent_users,
                "successful_requests": len(results),
                "failed_requests": len(errors),
                "total_time": round(total_time, 2),
                "requests_per_second": round(num_requests / total_time, 2),
                "avg_response_time": round(statistics.mean(results) * 1000, 2),  # ms
                "min_response_time": round(min(results) * 1000, 2),  # ms
                "max_response_time": round(max(results) * 1000, 2),  # ms
                "median_response_time": round(statistics.median(results) * 1000, 2),  # ms
                "std_dev": round(statistics.stdev(results) * 1000, 2) if len(results) > 1 else 0,
                "success_rate": round((len(results) / num_requests) * 100, 2),
                "errors": errors[:5]  # First 5 errors
            }
        else:
            stats = {
                "endpoint": endpoint,
                "error": "All requests failed",
                "errors": errors[:10]
            }
        
        self._print_load_test_results(stats)
        return stats
    
    def stress_test(self, endpoint: str, max_users: int = 100, 
                    step: int = 10, authenticated: bool = False) -> Dict:
        """
        Stress test: Find breaking point by gradually increasing load
        """
        print(f"\n{'='*60}")
        print(f"💪 STRESS TEST: {endpoint}")
        print(f"{'='*60}")
        print(f"Max Users: {max_users} | Step: {step}")
        
        stress_results = []
        breaking_point = None
        
        for users in range(step, max_users + 1, step):
            print(f"\n📊 Testing with {users} concurrent users...")
            
            results = []
            errors = 0
            
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=users) as executor:
                futures = [
                    executor.submit(self.measure_endpoint, "GET", endpoint, None, authenticated)
                    for _ in range(users * 2)  # 2 requests per user
                ]
                
                for future in as_completed(futures):
                    response_time, status_code, error = future.result()
                    
                    if status_code == 200:
                        results.append(response_time)
                    else:
                        errors += 1
            
            total_time = time.time() - start_time
            
            if results:
                avg_response = statistics.mean(results) * 1000
                success_rate = (len(results) / (users * 2)) * 100
                
                stress_results.append({
                    "concurrent_users": users,
                    "avg_response_time": round(avg_response, 2),
                    "success_rate": round(success_rate, 2),
                    "requests_per_second": round((users * 2) / total_time, 2)
                })
                
                print(f"  ✓ Avg Response: {avg_response:.2f}ms | Success: {success_rate:.1f}%")
                
                # Check if this is breaking point (>5s response or <95% success)
                if avg_response > 5000 or success_rate < 95:
                    breaking_point = users
                    print(f"  ⚠️ Breaking point detected at {users} users!")
                    break
            else:
                breaking_point = users
                print(f"  ❌ Complete failure at {users} users")
                break
        
        return {
            "endpoint": endpoint,
            "max_tested_users": max_users if not breaking_point else breaking_point,
            "breaking_point": breaking_point,
            "results": stress_results
        }
    
    def benchmark_endpoints(self, endpoints: List[Dict]) -> List[Dict]:
        """
        Benchmark multiple endpoints
        """
        print(f"\n{'='*60}")
        print(f"📈 ENDPOINT BENCHMARKS")
        print(f"{'='*60}")
        
        benchmarks = []
        
        for endpoint_config in endpoints:
            endpoint = endpoint_config['endpoint']
            authenticated = endpoint_config.get('authenticated', False)
            
            print(f"\n🎯 Testing: {endpoint}")
            
            # Warm-up request
            self.measure_endpoint("GET", endpoint, None, authenticated)
            
            # Measure 10 requests
            times = []
            for _ in range(10):
                response_time, status_code, error = self.measure_endpoint(
                    "GET", endpoint, None, authenticated
                )
                if status_code == 200:
                    times.append(response_time * 1000)  # Convert to ms
            
            if times:
                benchmark = {
                    "endpoint": endpoint,
                    "avg_time": round(statistics.mean(times), 2),
                    "min_time": round(min(times), 2),
                    "max_time": round(max(times), 2),
                    "median_time": round(statistics.median(times), 2),
                    "rating": self._rate_performance(statistics.mean(times) * 1000)
                }
                benchmarks.append(benchmark)
                
                print(f"  Avg: {benchmark['avg_time']}ms | Rating: {benchmark['rating']}")
            else:
                print(f"  ❌ All requests failed")
        
        return benchmarks
    
    def _rate_performance(self, avg_time_ms: float) -> str:
        """Rate endpoint performance"""
        if avg_time_ms < 100:
            return "⚡ Excellent"
        elif avg_time_ms < 300:
            return "✅ Good"
        elif avg_time_ms < 1000:
            return "⚠️ Acceptable"
        else:
            return "❌ Needs Optimization"
    
    def _print_load_test_results(self, stats: Dict):
        """Print formatted load test results"""
        if "error" in stats:
            print(f"\n❌ Test Failed: {stats['error']}")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 LOAD TEST RESULTS")
        print(f"{'='*60}")
        print(f"✅ Successful Requests: {stats['successful_requests']}/{stats['total_requests']}")
        print(f"❌ Failed Requests: {stats['failed_requests']}")
        print(f"📈 Success Rate: {stats['success_rate']}%")
        print(f"⚡ Requests/Second: {stats['requests_per_second']}")
        print(f"⏱️  Total Time: {stats['total_time']}s")
        print(f"\n📊 Response Times (ms):")
        print(f"  • Average: {stats['avg_response_time']}ms")
        print(f"  • Minimum: {stats['min_response_time']}ms")
        print(f"  • Maximum: {stats['max_response_time']}ms")
        print(f"  • Median: {stats['median_response_time']}ms")
        print(f"  • Std Dev: {stats['std_dev']}ms")
        
        # Performance rating
        if stats['avg_response_time'] < 100:
            rating = "⚡ Excellent"
        elif stats['avg_response_time'] < 300:
            rating = "✅ Good"
        elif stats['avg_response_time'] < 1000:
            rating = "⚠️ Acceptable"
        else:
            rating = "❌ Needs Optimization"
        
        print(f"\n🎯 Performance Rating: {rating}")
    
    def generate_report(self, results: Dict, output_file: str = "performance_report.json"):
        """Generate performance test report"""
        report = {
            "test_date": datetime.now().isoformat(),
            "base_url": self.base_url,
            "results": results,
            "summary": self._generate_summary(results)
        }
        
        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved to: {output_file}")
        
        # Print summary
        self._print_summary(report['summary'])
        
        return report
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate test summary"""
        summary = {
            "total_tests": len(results),
            "passed_tests": 0,
            "failed_tests": 0,
            "warnings": []
        }
        
        for test_name, test_result in results.items():
            if isinstance(test_result, dict):
                if "error" in test_result:
                    summary['failed_tests'] += 1
                elif "success_rate" in test_result and test_result['success_rate'] >= 95:
                    summary['passed_tests'] += 1
                else:
                    summary['passed_tests'] += 1
                    if test_result.get('success_rate', 100) < 100:
                        summary['warnings'].append(
                            f"{test_name}: {test_result.get('success_rate', 0)}% success rate"
                        )
        
        return summary
    
    def _print_summary(self, summary: Dict):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"📋 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        
        if summary['warnings']:
            print(f"\n⚠️ Warnings:")
            for warning in summary['warnings']:
                print(f"  • {warning}")


def run_comprehensive_tests():
    """Run comprehensive performance tests"""
    print("="*60)
    print("🚀 DOGGER 2.0 - COMPREHENSIVE PERFORMANCE TESTING")
    print("="*60)
    
    tester = PerformanceTester()
    
    # Authenticate first
    if not tester.authenticate():
        print("❌ Authentication failed. Make sure backend is running.")
        return
    
    results = {}
    
    # Test 1: Health endpoint (public, should be fastest)
    print("\n\n🔍 TEST 1: Health Endpoint Load Test")
    results['health_load_test'] = tester.load_test(
        endpoint="/api/health/",
        num_requests=100,
        concurrent_users=10,
        authenticated=False
    )
    
    # Test 2: Profile endpoint (authenticated)
    print("\n\n🔍 TEST 2: Profile Endpoint Load Test")
    results['profile_load_test'] = tester.load_test(
        endpoint="/api/profile/",
        num_requests=50,
        concurrent_users=5,
        authenticated=True
    )
    
    # Test 3: Stress test on health endpoint
    print("\n\n🔍 TEST 3: Health Endpoint Stress Test")
    results['health_stress_test'] = tester.stress_test(
        endpoint="/api/health/",
        max_users=50,
        step=10,
        authenticated=False
    )
    
    # Test 4: Benchmark all endpoints
    print("\n\n🔍 TEST 4: Endpoint Benchmarks")
    endpoints_to_test = [
        {"endpoint": "/api/health/", "authenticated": False},
        {"endpoint": "/api/profile/", "authenticated": True},
        {"endpoint": "/api/metrics/", "authenticated": True},
    ]
    results['benchmarks'] = tester.benchmark_endpoints(endpoints_to_test)
    
    # Generate report
    report = tester.generate_report(results)
    
    print("\n" + "="*60)
    print("✅ PERFORMANCE TESTING COMPLETE!")
    print("="*60)
    
    return report


if __name__ == "__main__":
    run_comprehensive_tests()