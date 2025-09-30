#!/usr/bin/env python3
"""Test script for universal design system"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.prompt_agent.universal_extractor import UniversalPromptExtractor

def test_universal_extractor():
    """Test the universal extractor with different design types"""
    extractor = UniversalPromptExtractor()
    
    test_prompts = [
        # Building designs
        "Design a 3-story office building with steel and glass, 20x15 meters",
        "Build a residential house with cement and bricks, 10m height",
        
        # Vehicle designs  
        "Design a luxury car with leather seats, GPS, and sunroof",
        "Create a truck with 300hp engine and cargo capacity of 5 tons",
        
        # Electronics designs
        "Design a laptop with 16GB RAM, touchscreen, and aluminum body",
        "Create a smartphone with wireless charging and face recognition",
        
        # Appliance designs
        "Design a smart fridge with energy efficiency and wifi control",
        "Create a washing machine with automatic timer and stainless steel drum",
        
        # Furniture designs
        "Design an ergonomic office chair with adjustable height and lumbar support",
        "Create a wooden dining table for 6 people with storage drawers",
        
        # Non-design prompts (should fail)
        "Tell me a story about a princess",
        "What's the weather like today?"
    ]
    
    print("Testing Universal Design Extractor")
    print("=" * 50)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Testing: '{prompt}'")
        print("-" * 40)
        
        try:
            spec = extractor.extract_spec(prompt)
            print(f"SUCCESS")
            print(f"   Design Type: {spec.design_type}")
            print(f"   Category: {spec.category}")
            print(f"   Materials: {[m.type for m in spec.materials]}")
            print(f"   Features: {spec.features[:3]}...")  # Show first 3 features
            print(f"   Components: {spec.components[:3]}...")  # Show first 3 components
            
        except ValueError as e:
            print(f"REJECTED: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    test_universal_extractor()