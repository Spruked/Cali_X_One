#!/usr/bin/env python3
"""
Cali_X_One Performance Benchmark Suite

Tests system performance under load and measures key metrics.
"""

import asyncio
import aiohttp
import time
import statistics
import json
from datetime import datetime
from typing import List, Dict, Any
import sys
import os

class PerformanceBenchmark:
    def __init__(self, base_url: str = "http://localhost:8003", concurrent_users: int = 10):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.results: Dict[str, Any] = {}

    async def run_benchmarks(self) -> Dict[str, Any]:
        """Run all performance benchmarks"""
        print("🏃 Cali_X_One Performance Benchmark Suite")
        print("=" * 60)

        benchmarks = [
            self.benchmark_micro_skg_speed,
            self.benchmark_uqv_throughput,
            self.benchmark_concurrent_queries,
            self.benchmark_worker_heartbeats,
            self.benchmark_vault_operations
        ]

        for benchmark_func in benchmarks:
            benchmark_name = benchmark_func.__name__.replace('benchmark_', '').replace('_', ' ').title()
            print(f"\n📈 Running: {benchmark_name}")
            print("-" * 40)

            try:
                start_time = time.time()
                result = await benchmark_func()
                duration = time.time() - start_time

                result['total_duration'] = duration
                self.results[benchmark_func.__name__] = result

                print(f"✅ Completed in {duration:.2f}s")
                self.print_benchmark_results(result)

            except Exception as e:
                print(f"❌ Benchmark failed: {e}")
                self.results[benchmark_func.__name__] = {'error': str(e)}

        self.generate_report()
        return self.results

    def print_benchmark_results(self, result: Dict[str, Any]):
        """Print formatted benchmark results"""
        if 'avg_response_time' in result:
            print(".2f"        if 'throughput' in result:
            print(".2f"        if 'success_rate' in result:
            print(".1f"        if 'p95_response_time' in result:
            print(".2f"
    async def benchmark_micro_skg_speed(self) -> Dict[str, Any]:
        """Benchmark micro-SKG clustering speed"""
        test_texts = [
            "grief leads to acceptance through transformation",
            "machine learning requires mathematical foundations",
            "consciousness emerges from complex information processing",
            "emotions drive human decision making processes",
            "knowledge graphs connect concepts through relationships"
        ]

        response_times = []

        async with aiohttp.ClientSession() as session:
            for text in test_texts:
                start_time = time.time()

                try:
                    async with session.post(
                        f"{self.base_url}/api/skg/cluster",
                        json={'text': text},
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as resp:
                        if resp.status == 200:
                            response_times.append((time.time() - start_time) * 1000)

                except Exception as e:
                    print(f"Request failed: {e}")

        if not response_times:
            return {'error': 'No successful requests'}

        return {
            'avg_response_time': statistics.mean(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'p95_response_time': statistics.quantiles(response_times, n=20)[18],  # 95th percentile
            'requests_completed': len(response_times),
            'target_max_time': 40,  # ms
            'within_target': all(t < 40 for t in response_times)
        }

    async def benchmark_uqv_throughput(self) -> Dict[str, Any]:
        """Benchmark UQV storage throughput"""
        test_queries = [
            {
                'user_id': f'bench_user_{i}',
                'query_text': f'how does concept {i} relate to AGI',
                'clusters_found': 0,
                'worker_name': 'benchmark_worker'
            }
            for i in range(50)
        ]

        response_times = []
        successful_requests = 0

        async with aiohttp.ClientSession() as session:
            for query_data in test_queries:
                start_time = time.time()

                try:
                    async with session.post(
                        f"{self.base_url}/api/uqv/store",
                        json=query_data,
                        timeout=aiohttp.ClientTimeout(total=2)
                    ) as resp:
                        if resp.status == 200:
                            response_times.append((time.time() - start_time) * 1000)
                            successful_requests += 1

                except Exception as e:
                    print(f"UQV request failed: {e}")

        if not response_times:
            return {'error': 'No successful requests'}

        return {
            'avg_response_time': statistics.mean(response_times),
            'throughput': successful_requests / (sum(response_times) / 1000),  # req/sec
            'success_rate': (successful_requests / len(test_queries)) * 100,
            'total_requests': len(test_queries),
            'successful_requests': successful_requests,
            'target_throughput': 10  # req/sec
        }

    async def benchmark_concurrent_queries(self) -> Dict[str, Any]:
        """Benchmark concurrent query handling"""
        async def single_query(session: aiohttp.ClientSession, query_id: int):
            query_data = {
                'query': f'what is the relationship between concept {query_id} and AGI',
                'user_id': f'concurrent_user_{query_id}'
            }

            start_time = time.time()
            try:
                async with session.post(
                    f"{self.base_url}/api/query",
                    json=query_data,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    return {
                        'success': resp.status == 200,
                        'response_time': (time.time() - start_time) * 1000,
                        'query_id': query_id
                    }
            except Exception as e:
                return {
                    'success': False,
                    'response_time': (time.time() - start_time) * 1000,
                    'query_id': query_id,
                    'error': str(e)
                }

        async with aiohttp.ClientSession() as session:
            # Run concurrent queries
            tasks = [single_query(session, i) for i in range(self.concurrent_users)]
            results = await asyncio.gather(*tasks)

        successful = [r for r in results if r['success']]
        response_times = [r['response_time'] for r in results]

        return {
            'concurrent_users': self.concurrent_users,
            'success_rate': (len(successful) / len(results)) * 100,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'throughput': len(successful) / (max(response_times) / 1000) if response_times else 0,
            'target_concurrent': 10,
            'target_response_time': 5000  # 5 seconds
        }

    async def benchmark_worker_heartbeats(self) -> Dict[str, Any]:
        """Benchmark worker heartbeat performance"""
        heartbeat_data = {
            'worker_id': 'benchmark_worker',
            'status': 'alive',
            'load': 0.5,
            'last_task': 'benchmarking'
        }

        response_times = []

        async with aiohttp.ClientSession() as session:
            for i in range(100):  # 100 heartbeat requests
                start_time = time.time()

                try:
                    async with session.post(
                        f"{self.base_url}/api/workers/heartbeat",
                        json=heartbeat_data,
                        timeout=aiohttp.ClientTimeout(total=1)
                    ) as resp:
                        if resp.status == 200:
                            response_times.append((time.time() - start_time) * 1000)

                except Exception as e:
                    print(f"Heartbeat failed: {e}")

        if not response_times:
            return {'error': 'No successful heartbeats'}

        return {
            'avg_response_time': statistics.mean(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'throughput': len(response_times) / (sum(response_times) / 1000),  # heartbeats/sec
            'total_heartbeats': len(response_times),
            'target_response_time': 50,  # ms
            'within_target': all(t < 50 for t in response_times)
        }

    async def benchmark_vault_operations(self) -> Dict[str, Any]:
        """Benchmark vault consciousness operations"""
        reflection_data = {
            'module': 'benchmark_reasoning',
            'insight': f'Benchmark insight {time.time()}',
            'context': {'benchmark': True, 'timestamp': time.time()}
        }

        response_times = []

        async with aiohttp.ClientSession() as session:
            for i in range(20):  # 20 reflection storage operations
                start_time = time.time()

                try:
                    async with session.post(
                        f"{self.base_url}/vault/reflections/add",
                        json=reflection_data,
                        timeout=aiohttp.ClientTimeout(total=2)
                    ) as resp:
                        if resp.status == 200:
                            response_times.append((time.time() - start_time) * 1000)

                except Exception as e:
                    print(f"Vault operation failed: {e}")

        if not response_times:
            return {'error': 'No successful vault operations'}

        return {
            'avg_response_time': statistics.mean(response_times),
            'throughput': len(response_times) / (sum(response_times) / 1000),  # operations/sec
            'total_operations': len(response_times),
            'target_response_time': 200,  # ms
            'within_target': all(t < 200 for t in response_times)
        }

    def generate_report(self):
        """Generate comprehensive benchmark report"""
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE BENCHMARK REPORT")
        print("=" * 60)

        # Overall summary
        benchmarks_run = len(self.results)
        benchmarks_passed = sum(1 for r in self.results.values() if 'error' not in r)

        print(f"Benchmarks Completed: {benchmarks_passed}/{benchmarks_run}")

        # Performance targets
        targets = {
            'micro_skg_speed': {'target': 40, 'unit': 'ms', 'metric': 'avg_response_time'},
            'uqv_throughput': {'target': 10, 'unit': 'req/sec', 'metric': 'throughput'},
            'concurrent_queries': {'target': 10, 'unit': 'concurrent', 'metric': 'concurrent_users'},
            'worker_heartbeats': {'target': 50, 'unit': 'ms', 'metric': 'avg_response_time'},
            'vault_operations': {'target': 200, 'unit': 'ms', 'metric': 'avg_response_time'}
        }

        print("\n🎯 Target Compliance:")
        for bench_name, target_info in targets.items():
            if bench_name in self.results:
                result = self.results[bench_name]
                if 'error' not in result:
                    actual = result.get(target_info['metric'], 0)
                    target = target_info['target']
                    unit = target_info['unit']

                    if target_info['metric'] == 'throughput':
                        passed = actual >= target
                    else:
                        passed = actual <= target

                    status = "✅" if passed else "❌"
                    print(".2f"
        # Save detailed results
        self.save_benchmark_results()

        print("\n📄 Detailed results saved to: benchmark_results.json")

    def save_benchmark_results(self):
        """Save benchmark results to JSON file"""
        results_file = os.path.join(os.path.dirname(__file__), 'benchmark_results.json')

        results_data = {
            'timestamp': datetime.now().isoformat(),
            'concurrent_users': self.concurrent_users,
            'results': self.results
        }

        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)


async def main():
    """Main benchmark runner"""
    print("Cali_X_One Performance Benchmark Suite")
    print("Testing against:", "http://localhost:8003")

    # Check if server is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8003/health', timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status != 200:
                    print("❌ Server not responding. Please start the server first:")
                    print("   python run_server.py")
                    return
    except:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python run_server.py")
        return

    # Run benchmarks
    benchmark = PerformanceBenchmark(concurrent_users=10)
    results = await benchmark.run_benchmarks()

    print("\n🏁 Benchmarking complete!")


if __name__ == "__main__":
    asyncio.run(main())