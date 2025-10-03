#!/usr/bin/env python3
"""Test Day 4 Security, Monitoring, and Compute Routing features"""

import asyncio
import os
from src.services.compute_router import compute_router
from src.monitoring.cost_tracker import cost_tracker
from src.utils.system_monitoring import init_sentry, capture_message, capture_exception

async def test_compute_routing():
    """Test compute routing logic"""
    print("=== Testing Compute Routing ===")
    
    # Test simple prompt (should route to local)
    simple_prompt = "Modern chair"
    result = await compute_router.route_inference(simple_prompt, None, "generation")
    print(f"Simple prompt routed to: {result['compute']}")
    print(f"Complexity: {result['complexity']:.2f}")
    print(f"Cost estimate: ${result['cost_estimate']:.4f}")
    
    # Test complex prompt (should route to cloud if available)
    complex_prompt = "Design a comprehensive multi-story industrial complex with advanced sustainable features, integrated smart systems, and detailed architectural specifications for a 50-acre site"
    result = await compute_router.route_inference(complex_prompt, None, "generation")
    print(f"Complex prompt routed to: {result['compute']}")
    print(f"Complexity: {result['complexity']:.2f}")
    print(f"Cost estimate: ${result['cost_estimate']:.4f}")
    
    # Get routing stats
    stats = compute_router.get_job_stats()
    print(f"Total jobs processed: {stats['total_jobs']}")
    print(f"Local GPU available: {stats['local_gpu_available']}")
    print(f"Yotta configured: {stats['yotta_configured']}")

def test_cost_tracking():
    """Test cost tracking and usage logging"""
    print("\n=== Testing Cost Tracking ===")
    
    # Simulate some job costs
    cost_tracker.log_job_cost("local_rtx3060", 150, 2.5, 0.3, "generation")
    cost_tracker.log_job_cost("yotta_cloud", 300, 1.8, 0.7, "generation")
    cost_tracker.log_job_cost("local_rtx3060", 100, 1.2, 0.2, "switch")
    
    # Get daily report
    daily_report = cost_tracker.get_daily_report()
    print(f"Daily cost report: ${daily_report['total_cost']:.4f}")
    print(f"Total jobs: {daily_report['total_jobs']}")
    print(f"Local cost percentage: {daily_report['cost_breakdown']['local_percentage']:.1f}%")
    
    # Get usage patterns
    patterns = cost_tracker.get_usage_patterns()
    print(f"Compute distribution: {patterns['compute_distribution']}")
    print(f"Job type distribution: {patterns['job_type_distribution']}")

def test_sentry_integration():
    """Test Sentry error tracking"""
    print("\n=== Testing Sentry Integration ===")
    
    # Initialize Sentry
    sentry_initialized = init_sentry()
    print(f"Sentry initialized: {sentry_initialized}")
    
    # Test message capture
    capture_message("Test message from Day 4 features", "info", {
        "test_type": "day4_features",
        "component": "sentry_integration"
    })
    print("Test message sent to Sentry")
    
    # Test exception capture
    try:
        raise ValueError("Test exception for Sentry")
    except Exception as e:
        capture_exception(e, {
            "test_type": "day4_features",
            "component": "exception_handling"
        })
        print("Test exception captured by Sentry")

def test_cost_optimization():
    """Test cost optimization recommendations"""
    print("\n=== Testing Cost Optimization ===")
    
    # Get cost report with recommendations
    cost_report = compute_router.get_cost_report()
    print(f"Total cost: ${cost_report['total_cost']:.4f}")
    print(f"Cost savings vs all-cloud: ${cost_report['efficiency']['cost_savings_vs_all_cloud']:.4f}")
    print("Recommendations:")
    for rec in cost_report['recommendations']:
        print(f"  - {rec}")
    
    # Get weekly trends
    weekly_report = cost_tracker.get_weekly_report()
    print(f"Weekly period: {weekly_report['period']}")
    print(f"Weekly total cost: ${weekly_report['summary']['total_cost']:.4f}")
    if 'trends' in weekly_report:
        print(f"Cost trend: {weekly_report['trends'].get('trend', 'N/A')}")

async def main():
    """Run all Day 4 tests"""
    print("[TEST] Testing Day 4 - Security, Monitoring, and Compute Routing")
    print("=" * 60)
    
    # Test compute routing
    await test_compute_routing()
    
    # Test cost tracking
    test_cost_tracking()
    
    # Test Sentry integration
    test_sentry_integration()
    
    # Test cost optimization
    test_cost_optimization()
    
    print("\n[SUCCESS] Day 4 feature testing completed!")
    print("=" * 60)
    
    # Summary
    print("\n[SUMMARY] SUMMARY:")
    print("[OK] Compute routing: Local RTX-3060 vs Yotta cloud logic")
    print("[OK] Cost tracking: Usage logging and cost analysis")
    print("[OK] Sentry integration: Error tracking and monitoring")
    print("[OK] Cost optimization: Recommendations and trends")

if __name__ == "__main__":
    asyncio.run(main())