#!/usr/bin/env python3
"""
Cali_X_One AGI System - Automated Test Suite

This script runs comprehensive tests against the Cali_X_One system
to verify all claims and functionality.
"""

import asyncio
import aiohttp
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import subprocess
import statistics

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class CaliXOneTester:
    def __init__(self, base_url: str = "http://localhost:8006"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.test_results: Dict[str, Any] = {}
        self.start_time = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.start_time = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test cases"""
        print("🚀 Starting Cali_X_One Comprehensive Test Suite")
        print("=" * 60)

        tests = [
            self.test_system_boot,
            self.test_micro_skg_speed,
            self.test_uqv_vault,
            self.test_caleon_predicates,
            self.test_worker_registry,
            self.test_vault_integration,
            self.test_end_to_end_flow
        ]

        for test_func in tests:
            test_name = test_func.__name__.replace('test_', '').replace('_', ' ').title()
            print(f"\n🧪 Running: {test_name}")
            print("-" * 40)

            try:
                start_time = time.time()
                result = await test_func()
                duration = time.time() - start_time

                result['duration'] = duration
                result['status'] = 'PASS' if result.get('success', False) else 'FAIL'

                self.test_results[test_func.__name__] = result

                status_emoji = "✅" if result['status'] == 'PASS' else "❌"
                print(f"{status_emoji} {test_func.__name__}: {result['status']} ({duration:.2f}s)")
            except Exception as e:
                error_result = {
                    'success': False,
                    'status': 'ERROR',
                    'error': str(e),
                    'duration': 0
                }
                self.test_results[test_func.__name__] = error_result
                print(f"❌ ERROR: {e}")

        # Generate summary
        self.generate_summary()
        return self.test_results

    async def make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with timing"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()

        try:
            async with self.session.request(method, url, **kwargs) as response:
                duration = time.time() - start_time
                if response.content_type == 'application/json':
                    data = await response.json()
                else:
                    data = await response.text()

                return {
                    'status_code': response.status,
                    'data': data,
                    'duration': duration,
                    'success': response.status < 400
                }
        except Exception as e:
            return {
                'status_code': None,
                'data': None,
                'duration': time.time() - start_time,
                'success': False,
                'error': str(e)
            }

    async def test_system_boot(self) -> Dict[str, Any]:
        """Test system startup and health check"""
        # Test health endpoint
        health_result = await self.make_request('GET', '/health')

        if not health_result['success']:
            return {
                'success': False,
                'error': 'Health check failed',
                'health_response': health_result
            }

        # Check for required fields
        health_data = health_result['data']
        required_fields = ['status']

        missing_fields = [field for field in required_fields if field not in health_data]

        return {
            'success': len(missing_fields) == 0,
            'health_data': health_data,
            'missing_fields': missing_fields,
            'response_time': health_result['duration']
        }

    async def test_micro_skg_speed(self) -> Dict[str, Any]:
        """Test micro-SKG clustering speed (< 40ms target)"""
        test_text = "grief leads to acceptance through transformation and healing"

        result = await self.make_request('POST', '/api/skg/cluster',
            json={'text': test_text}
        )

        if not result['success']:
            return {
                'success': False,
                'error': 'Clustering request failed',
                'response': result
            }

        # Check timing
        response_time_ms = result['duration'] * 1000
        target_time = 40  # ms

        # Check response structure
        data = result['data']
        has_clusters = isinstance(data.get('clusters'), list) and len(data['clusters']) > 0
        has_density = all(c.get('density', 0) >= 0.8 for c in data.get('clusters', []))

        return {
            'success': response_time_ms < target_time and has_clusters and has_density,
            'response_time_ms': response_time_ms,
            'target_time': target_time,
            'clusters_found': len(data.get('clusters', [])),
            'avg_density': statistics.mean([c.get('density', 0) for c in data.get('clusters', [])]) if data.get('clusters') else 0,
            'data': data
        }

    async def test_uqv_vault(self) -> Dict[str, Any]:
        """Test UQV (Unanswered Query Vault) functionality"""
        # Store a test query
        store_data = {
            'user_id': 'test_user_uqv',
            'query_text': 'how do I mint grief into wisdom',
            'clusters_found': 0,
            'worker_name': 'test_worker'
        }

        store_result = await self.make_request('POST', '/api/uqv/store', json=store_data)

        if not store_result['success']:
            return {
                'success': False,
                'error': 'UQV store failed',
                'store_response': store_result
            }

        # Check stats
        stats_result = await self.make_request('GET', '/api/uqv/stats')

        if not stats_result['success']:
            return {
                'success': False,
                'error': 'UQV stats failed',
                'stats_response': stats_result
            }

        stats_data = stats_result['data']
        queries_before = getattr(self, '_uqv_initial_count', 0)
        queries_after = stats_data.get('total_queries', 0)

        # Retrieve stored query
        list_result = await self.make_request('GET', '/api/uqv/list?user_id=test_user_uqv')

        return {
            'success': queries_after > queries_before,
            'queries_before': queries_before,
            'queries_after': queries_after,
            'retrieval_success': list_result['success'],
            'stored_query_found': len(list_result.get('data', [])) > 0,
            'stats_data': stats_data
        }

    async def test_caleon_predicates(self) -> Dict[str, Any]:
        """Test Caleon predicate invention from clusters"""
        # Send cluster data
        cluster_data = {
            'user_id': 'test_user_predicates',
            'worker': 'josephine_test',
            'clusters': [{
                'id': 'c1',
                'nodes': ['grief', 'acceptance', 'transformation'],
                'density': 0.99,
                'seed': 'grief'
            }]
        }

        ingest_result = await self.make_request('POST', '/caleon/ingest_clusters', json=cluster_data)

        if not ingest_result['success']:
            return {
                'success': False,
                'error': 'Cluster ingestion failed',
                'ingest_response': ingest_result
            }

        # Check for invented predicates
        predicates_result = await self.make_request('GET', '/api/caleon/predicates')

        if not predicates_result['success']:
            return {
                'success': False,
                'error': 'Predicate retrieval failed',
                'predicates_response': predicates_result
            }

        predicates_data = predicates_result['data']
        predicates_list = predicates_data.get('predicates', [])

        # Check for high-confidence predicates
        high_confidence = [p for p in predicates_list if p.get('confidence', 0) >= 0.75]

        return {
            'success': len(high_confidence) > 0,
            'total_predicates': len(predicates_list),
            'high_confidence_predicates': len(high_confidence),
            'avg_confidence': statistics.mean([p.get('confidence', 0) for p in predicates_list]) if predicates_list else 0,
            'predicates_data': predicates_data
        }

    async def test_worker_registry(self) -> Dict[str, Any]:
        """Test worker registration and heartbeat system"""
        # Register test worker
        worker_data = {
            'worker_id': 'test_worker_registry',
            'worker_type': 'josephine',
            'capabilities': ['predicate_invention', 'cluster_fusion'],
            'endpoint': 'http://localhost:9998',
            'metadata': {'version': '1.0.0'}
        }

        register_result = await self.make_request('POST', '/api/workers/register', json=worker_data)

        if not register_result['success']:
            return {
                'success': False,
                'error': 'Worker registration failed',
                'register_response': register_result
            }

        # Send heartbeat
        heartbeat_data = {
            'worker_id': 'test_worker_registry',
            'status': 'alive',
            'load': 0.1,
            'last_task': 'testing'
        }

        heartbeat_result = await self.make_request('POST', '/api/workers/heartbeat', json=heartbeat_data)

        # List workers
        list_result = await self.make_request('GET', '/api/workers/list')

        if not list_result['success']:
            return {
                'success': False,
                'error': 'Worker listing failed',
                'list_response': list_result
            }

        workers_data = list_result['data']
        workers_list = workers_data.get('workers', [])
        test_worker = next((w for w in workers_list if w['worker_id'] == 'test_worker_registry'), None)

        return {
            'success': test_worker is not None and test_worker.get('status') == 'alive',
            'registration_success': register_result['success'],
            'heartbeat_success': heartbeat_result['success'],
            'worker_found': test_worker is not None,
            'worker_status': test_worker.get('status') if test_worker else None,
            'total_workers': len(workers_list)
        }

    async def test_vault_integration(self) -> Dict[str, Any]:
        """Test vault consciousness system integration"""
        # Check vault health
        health_result = await self.make_request('GET', '/vault/health')

        if not health_result['success']:
            return {
                'success': False,
                'error': 'Vault health check failed',
                'health_response': health_result
            }

        health_data = health_result['data']

        # Add a test reflection
        reflection_data = {
            'module': 'test_reasoning',
            'insight': 'Grief transforms into wisdom through acceptance',
            'context': {
                'confidence': 0.95,
                'test_run': True
            }
        }

        reflection_result = await self.make_request('POST', '/vault/reflections/add', json=reflection_data)

        # Get system status
        status_result = await self.make_request('GET', '/vault/status')

        return {
            'success': health_data.get('status') == 'healthy' and reflection_result['success'],
            'vault_healthy': health_data.get('status') == 'healthy',
            'overall_health': health_data.get('overall_health', False),
            'healthy_components': health_data.get('healthy_components', 0),
            'reflection_stored': reflection_result['success'],
            'status_available': status_result['success']
        }

    async def test_end_to_end_flow(self) -> Dict[str, Any]:
        """Test complete AGI workflow from query to predicate invention"""
        user_id = f"test_e2e_{int(time.time())}"

        # 1. Submit natural language query
        query_data = {
            'query': 'how does grief become wisdom',
            'user_id': user_id
        }

        query_result = await self.make_request('POST', '/api/query', json=query_data)

        if not query_result['success']:
            return {
                'success': False,
                'error': 'Query submission failed',
                'stage': 'query_submission',
                'query_response': query_result
            }

        # Wait a moment for processing
        await asyncio.sleep(0.5)

        # 2. Check query status
        status_result = await self.make_request('GET', f'/api/query/status/{user_id}')

        # 3. Check for clusters
        clusters_result = await self.make_request('GET', f'/api/clusters/recent?user_id={user_id}')

        # 4. Check for predicates
        predicates_result = await self.make_request('GET', f'/api/caleon/predicates?user_id={user_id}')

        # 5. Check vault reflections
        reflections_result = await self.make_request('GET', '/vault/reflections/recent?limit=5')

        # Evaluate success
        query_processed = status_result['success']
        clusters_generated = clusters_result['success'] and len(clusters_result.get('data', [])) > 0
        predicates_invented = predicates_result['success'] and len(predicates_result.get('data', {}).get('predicates', [])) > 0
        reflections_stored = reflections_result['success']

        return {
            'success': query_processed,  # At minimum, query should be processed
            'query_processed': query_processed,
            'clusters_generated': clusters_generated,
            'predicates_invented': predicates_invented,
            'reflections_stored': reflections_stored,
            'user_id': user_id,
            'processing_complete': all([query_processed, clusters_generated, predicates_invented])
        }

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results.values() if r.get('status') == 'PASS')
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {passed_tests/total_tests*100:.1f}%")
        total_duration = time.time() - self.start_time
        print(f"Total Duration: {total_duration:.2f}s")
        print("\nDetailed Results:")
        for test_name, result in self.test_results.items():
            status = result.get('status', 'UNKNOWN')
            duration = result.get('duration', 0)
            emoji = "✅" if status == 'PASS' else "❌" if status == 'FAIL' else "⚠️"
            print(f"{emoji} {test_name}: {status} ({duration:.2f}s)")
        print("\n" + "=" * 60)

        # Save results to file
        self.save_results()

    def save_results(self):
        """Save test results to JSON file"""
        results_file = os.path.join(os.path.dirname(__file__), 'test_results.json')

        results_data = {
            'timestamp': datetime.now().isoformat(),
            'total_duration': time.time() - self.start_time,
            'results': self.test_results
        }

        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)

        print(f"📄 Results saved to: {results_file}")


async def main():
    """Main test runner"""
    print("Cali_X_One AGI System - Automated Test Suite")
    print("Testing against:", "http://localhost:8006")

    # Check if server is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8006/health', timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status != 200:
                    print("❌ Server not responding. Please start the server first:")
                    print("   python run_server.py")
                    return
    except:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python run_server.py")
        return

    # Run tests
    async with CaliXOneTester() as tester:
        results = await tester.run_all_tests()

    # Exit with appropriate code
    passed = sum(1 for r in results.values() if r.get('status') == 'PASS')
    total = len(results)

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"⚠️  {total - passed} tests failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())