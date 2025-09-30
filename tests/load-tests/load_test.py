"""Load testing for 50 concurrent users"""

import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def make_request(session, url, data, headers=None):
    """Make HTTP request"""
    try:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}

async def get_auth_token(base_url="https://prompt-to-json-backend.onrender.com"):
    """Get JWT token for authentication"""
    import os
    token_url = f"{base_url}/token"
    token_data = {
        "username": os.getenv("DEMO_USERNAME", "demo"),
        "password": os.getenv("DEMO_PASSWORD", "demo123")
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, json=token_data) as response:
            if response.status == 200:
                result = await response.json()
                return result["access_token"]
            return None

async def load_test_50_users():
    """Simulate 50 concurrent users testing public endpoint"""
    base_url = "https://prompt-to-json-backend.onrender.com"
    url = f"{base_url}/metrics"
    
    print(f"Testing production server: {base_url}")
    print("Using public /metrics endpoint (no auth required)")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(50):
            task = session.get(url)
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        success_count = sum(1 for r in responses if hasattr(r, 'status') and r.status == 200)
        
        print(f"\n🚀 PRODUCTION LOAD TEST RESULTS")
        print(f"═══════════════════════════════")
        print(f"✅ Successful: {success_count}/50")
        print(f"❌ Failed: {50 - success_count}/50")
        print(f"⏱️  Total time: {end_time - start_time:.2f}s")
        print(f"📊 Requests/second: {50 / (end_time - start_time):.2f}")
        print(f"🎯 Production server is {'HEALTHY' if success_count > 45 else 'DEGRADED'}")
        
        # Close responses
        for r in responses:
            if hasattr(r, 'close'):
                r.close()

async def comprehensive_load_test():
    """Test system under 1000+ concurrent users"""
    from statistics import mean
    
    results = {
        'response_times': [],
        'successful_requests': 0,
        'failed_requests': 0
    }
    
    url = "https://prompt-to-json-backend.onrender.com/generate"
    data = {"prompt": "Modern office building"}
    headers = {"X-API-Key": "bhiv-secret-key-2024"}
    
    async def test_single_request():
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as resp:
                    if resp.status == 200:
                        results['successful_requests'] += 1
                    else:
                        results['failed_requests'] += 1
                    
                    response_time = time.time() - start_time
                    results['response_times'].append(response_time)
        except Exception:
            results['failed_requests'] += 1
    
    # Run 1000 concurrent requests
    tasks = [test_single_request() for _ in range(1000)]
    start_time = time.time()
    await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    # Calculate metrics
    if results['response_times']:
        avg_response_time = mean(results['response_times'])
        p95_response_time = sorted(results['response_times'])[int(0.95 * len(results['response_times']))]
    else:
        avg_response_time = 0
        p95_response_time = 0
    
    print(f"""
🔥 LOAD TEST RESULTS - 1000 CONCURRENT USERS
═══════════════════════════════════════════
✅ Successful Requests: {results['successful_requests']}
❌ Failed Requests: {results['failed_requests']}
📊 Success Rate: {results['successful_requests']/1000*100:.1f}%
⏱️  Average Response Time: {avg_response_time:.3f}s
📈 95th Percentile: {p95_response_time:.3f}s
🚀 Requests/Second: {1000/total_time:.0f}
""")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--comprehensive":
        asyncio.run(comprehensive_load_test())
    else:
        asyncio.run(load_test_50_users())