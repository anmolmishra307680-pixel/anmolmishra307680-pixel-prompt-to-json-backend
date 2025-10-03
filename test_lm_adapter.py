#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the standardized LM adapter interface"""

from src.core.lm_adapter import LocalLMAdapter
from src.agents.main_agent import MainAgent

def test_lm_adapter_interface():
    """Test standardized lm.run(prompt, params) interface"""
    
    # Test direct LM adapter
    print("=== Testing Direct LM Adapter ===")
    lm = LocalLMAdapter()
    
    # Test with basic prompt
    result1 = lm.run("Smart home IoT sensor with WiFi")
    print(f"Design Type: {result1['design_type']}")
    print(f"Category: {result1['category']}")
    print(f"Objects: {len(result1.get('objects', []))} with IDs")
    print(f"Materials: {len(result1.get('materials', []))} with properties")
    
    # Test with parameters
    params = {"temperature": 0.8, "max_tokens": 512}
    result2 = lm.run("Sustainable office building with green roof", params)
    print(f"\nWith params - Design Type: {result2['design_type']}")
    print(f"Features: {result2.get('features', [])}")
    
    # Test MainAgent with standardized interface
    print("\n=== Testing MainAgent with LM Adapter ===")
    agent = MainAgent()
    
    spec = agent.run("Electric sports car with 400-mile range")
    print(f"MainAgent - Design Type: {spec.design_type}")
    print(f"MainAgent - Category: {spec.category}")
    print(f"MainAgent - Objects: {len(spec.objects) if spec.objects else 0}")
    print(f"MainAgent - Editable: {getattr(spec.metadata, 'editable', False)}")
    
    print("\n[SUCCESS] LM Adapter interface tests completed successfully!")

if __name__ == "__main__":
    test_lm_adapter_interface()