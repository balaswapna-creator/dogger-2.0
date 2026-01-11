"""
Simplified Performance Testing for Dogger 2.0
Tests public endpoints only (no authentication issues)
"""

import time
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def measure_request(url: str) -> tuple:
    """Measure single request time"""
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        elapsed = time.time() - start
        return elapsed, response.status_code, None
    except Exception as e:
        return time.time() - start, 0, str(e)


def load_test(url: str, num_requests: int = 100, concurrent: int = 10):
    """Simple load test"""
    print(f"\n{'='*60}")
    print(f"🔄 LOAD TEST: {url}")
    print(f"{'='*60}")
    print(f"Requests: {num_requests} | Concurrent: {concurrent}")
    
    results = []
    errors = []
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = [executor.submit(measure_request, url) for _ in range(num_requests)]
        
        for i, future in enumerate(as_completed(futures), 1):
            elapsed, status, error = future.result()
            
            if status == 200:
                results.append(elapsed * 1000)  # Convert to ms
            else:
                errors.append({"status": status, "error": error})
            
            if i % 10 == 0:
                print(f"  ✓ {i}/{num_requests} completed")
    
    total_time = time.time() - start_time
    
    if not results:
        print("\n❌ All requests failed!")
        return None
    
    # Calculate stats
    stats = {
        "url": url,
        "total_requests": num_requests,
        "successful": len(results),
        "failed": len(errors),
        "success_rate": round((len(results) / num_requests) * 100, 2),
        "requests_per_second": round(num_requests / total_time, 2),
        "total_time": round(total_time, 2),
        "avg_ms": round(statistics.mean(results), 2),
        "min_ms": round(min(results), 2),
        "max_ms": round(max(results), 2),
        "median_ms": round(statistics.median(results), 2),
        "std_dev": round(statistics.stdev(results), 2) if len(results) > 1 else 0
    }
    
    # Print results
    print(f"\n{'='*60}")
    print(f"📊 RESULTS")
    print(f"{'='*60}")
    print(f"✅ Successful: {stats['successful']}/{stats['total_requests']}")
    print(f"📈 Success Rate: {stats['success_rate']}%")
    print(f"⚡ Requests/sec: {stats['requests_per_second']}")
    print(f"⏱️  Total Time: {stats['total_time']}s")
    print(f"\n📊 Response Times (ms):")
    print(f"  • Average: {stats['avg_ms']}ms")
    print(f"  • Min: {stats['min_ms']}ms")
    print(f"  • Max: {stats['max_ms']}ms")
    print(f"  • Median: {stats['median_ms']}ms")
    print(f"  • Std Dev: {stats['std_dev']}ms")
    
    # Rating
    if stats['avg_ms'] < 100:
        rating = "⚡ Excellent"
    elif stats['avg_ms'] < 300:
        rating = "✅ Good"
    elif stats['avg_ms'] < 1000:
        rating = "⚠️ Acceptable"
    else:
        rating = "❌ Needs Optimization"
    
    print(f"\n🎯 Performance: {rating}")
    
    return stats


def stress_test(url: str, max_users: int = 50, step: int = 10):
    """Find breaking point"""
    print(f"\n{'='*60}")
    print(f"💪 STRESS TEST: {url}")
    print(f"{'='*60}")
    
    results = []
    breaking_point = None
    
    for users in range(step, max_users + 1, step):
        print(f"\n📊 Testing {users} concurrent users...")
        
        times = []
        errors = 0
        
        with ThreadPoolExecutor(max_workers=users) as executor:
            futures = [executor.submit(measure_request, url) for _ in range(users * 2)]
            
            for future in as_completed(futures):
                elapsed, status, error = future.result()
                if status == 200:
                    times.append(elapsed * 1000)
                else:
                    errors += 1
        
        if not times:
            print(f"  ❌ Complete failure!")
            breaking_point = users
            break
        
        avg_ms = statistics.mean(times)
        success_rate = (len(times) / (users * 2)) * 100
        
        results.append({
            "users": users,
            "avg_ms": round(avg_ms, 2),
            "success_rate": round(success_rate, 2)
        })
        
        print(f"  ✓ Avg: {avg_ms:.1f}ms | Success: {success_rate:.1f}%")
        
        # Check if breaking point
        if avg_ms > 5000 or success_rate < 95:
            breaking_point = users
            print(f"  ⚠️ Breaking point detected!")
            break
    
    print(f"\n{'='*60}")
    print(f"📊 STRESS TEST RESULTS")
    print(f"{'='*60}")
    print(f"Max Tested: {max_users if not breaking_point else breaking_point} users")
    if breaking_point:
        print(f"⚠️ Breaking Point: {breaking_point} concurrent users")
    else:
        print(f"✅ Stable up to {max_users} concurrent users")
    
    return {"max_tested": max_users if not breaking_point else breaking_point, 
            "breaking_point": breaking_point, "results": results}


def benchmark_endpoint(url: str, name: str):
    """Quick benchmark"""
    print(f"\n🎯 Benchmarking: {name}")
    
    # Warm up
    measure_request(url)
    
    # Measure 10 times
    times = []
    for _ in range(10):
        elapsed, status, _ = measure_request(url)
        if status == 200:
            times.append(elapsed * 1000)
    
    if not times:
        print(f"  ❌ Failed")
        return None
    
    avg = round(statistics.mean(times), 2)
    
    if avg < 100:
        rating = "⚡"
    elif avg < 300:
        rating = "✅"
    elif avg < 1000:
        rating = "⚠️"
    else:
        rating = "❌"
    
    print(f"  {rating} {avg}ms average")
    return {"name": name, "avg_ms": avg}


def main():
    """Run all performance tests"""
    print("="*60)
    print("🚀 DOGGER 2.0 - PERFORMANCE TESTING")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Health Endpoint Load Test
    print("\n\n🧪 TEST 1: Health Endpoint Load Test")
    health_load = load_test(f"{base_url}/api/health/", num_requests=100, concurrent=10)
    
    # Test 2: Health Endpoint Stress Test  
    print("\n\n🧪 TEST 2: Health Endpoint Stress Test")
    health_stress = stress_test(f"{base_url}/api/health/", max_users=50, step=10)
    
    # Test 3: Benchmark
    print("\n\n🧪 TEST 3: Endpoint Benchmarks")
    print("="*60)
    benchmarks = []
    benchmarks.append(benchmark_endpoint(f"{base_url}/api/health/", "Health Check"))
    
    # Summary
    print(f"\n\n{'='*60}")
    print("✅ TESTING COMPLETE!")
    print(f"{'='*60}")
    
    if health_load:
        print(f"\n📊 Health Endpoint Performance:")
        print(f"  • Average Response: {health_load['avg_ms']}ms")
        print(f"  • Success Rate: {health_load['success_rate']}%")
        print(f"  • Throughput: {health_load['requests_per_second']} req/s")
    
    if health_stress and health_stress['breaking_point']:
        print(f"\n💪 Stress Test:")
        print(f"  • Breaking Point: {health_stress['breaking_point']} users")
    else:
        print(f"\n💪 Stress Test:")
        print(f"  • Stable up to 50+ concurrent users ✅")
    
    print(f"\n⏱️  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


if __name__ == "__main__":
    main()