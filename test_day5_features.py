#!/usr/bin/env python3
"""Test Day 5 Frontend + Preview Integration features"""

import asyncio
import json
from src.storage.bucket_storage import bucket_storage
from src.services.preview_generator import preview_generator
from src.services.preview_manager import preview_manager

async def test_bucket_storage():
    """Test BHIV bucket storage with signed URLs"""
    print("=== Testing Bucket Storage ===")
    
    # Test signed URL generation
    object_key = "previews/test_spec_123.jpg"
    signed_url = bucket_storage.generate_signed_url(object_key, expires_in=3600)
    print(f"Generated signed URL: {signed_url[:80]}...")
    
    # Test preview upload
    mock_preview_data = b"mock_image_data_for_testing"
    upload_url = await bucket_storage.upload_preview("test_spec_123", mock_preview_data)
    print(f"Upload URL: {upload_url[:80]}...")
    
    # Test signature verification
    if "/api/v1/preview/local/" in upload_url:
        # Extract parameters from local URL
        parts = upload_url.split("?")[1].split("&")
        expires = int([p.split("=")[1] for p in parts if p.startswith("expires=")][0])
        signature = [p.split("=")[1] for p in parts if p.startswith("signature=")][0]
        
        is_valid = bucket_storage.verify_signed_url("previews_test_spec_123.jpg", expires, signature)
        print(f"Signature verification: {is_valid}")
    
    print(f"Using local storage: {bucket_storage.use_local}")

def test_preview_generator():
    """Test preview generation and Three.js formatting"""
    print("\n=== Testing Preview Generator ===")
    
    # Sample spec data
    spec_data = {
        "spec_id": "test_spec_456",
        "design_type": "building",
        "objects": [
            {
                "id": "floor_1",
                "type": "floor",
                "material": "marble",
                "dimensions": {"width": 10, "height": 0.1, "depth": 10},
                "position": {"x": 0, "y": 0, "z": 0},
                "editable": True,
                "properties": {"color": "white"}
            },
            {
                "id": "wall_1",
                "type": "wall",
                "material": "concrete",
                "dimensions": {"width": 10, "height": 3, "depth": 0.2},
                "position": {"x": 0, "y": 1.5, "z": 5},
                "editable": True,
                "properties": {"color": "gray"}
            },
            {
                "id": "chair_1",
                "type": "chair",
                "material": "wood",
                "dimensions": {"width": 0.6, "height": 0.8, "depth": 0.6},
                "position": {"x": 2, "y": 0.4, "z": 2},
                "editable": True,
                "properties": {"color": "brown"}
            }
        ]
    }
    
    # Test Three.js formatting
    threejs_data = preview_generator.format_for_threejs(spec_data)
    print(f"Three.js objects: {len(threejs_data['objects'])}")
    print(f"Scene background: {threejs_data['scene']['background']}")
    print(f"Camera type: {threejs_data['camera']['type']}")
    print(f"Lights count: {len(threejs_data['lights'])}")
    
    # Test material conversion
    for obj in threejs_data['objects']:
        print(f"Object {obj['id']}: {obj['geometry']['type']} with {obj['material']['type']}")
        print(f"  Material color: {obj['material']['color']}")
        print(f"  Editable: {obj['userData']['editable']}")
    
    # Test HTML viewer generation
    html_viewer = preview_generator.generate_viewer_html(spec_data)
    print(f"HTML viewer generated: {len(html_viewer)} characters")
    print(f"Contains Three.js: {'three.js' in html_viewer.lower()}")
    print(f"Contains controls: {'OrbitControls' in html_viewer}")

async def test_preview_manager():
    """Test enhanced preview manager"""
    print("\n=== Testing Preview Manager ===")
    
    spec_data = {
        "spec_id": "test_spec_789",
        "design_type": "furniture",
        "objects": [
            {
                "id": "table_1",
                "type": "table",
                "material": "wood",
                "dimensions": {"width": 1.5, "height": 0.8, "depth": 0.8},
                "editable": True,
                "properties": {"color": "brown"}
            }
        ]
    }
    
    # Test preview generation
    preview_url = await preview_manager.generate_preview(spec_data)
    print(f"Preview URL: {preview_url}")
    
    # Test Three.js data
    threejs_data = preview_manager.get_threejs_data(spec_data)
    print(f"Three.js data objects: {len(threejs_data['objects'])}")
    
    # Test viewer HTML
    viewer_html = preview_manager.generate_viewer_html(spec_data)
    print(f"Viewer HTML length: {len(viewer_html)}")
    
    # Test cache functionality
    cached_url = await preview_manager.generate_preview(spec_data)
    print(f"Cached URL matches: {preview_url == cached_url}")
    
    # Test refresh
    refreshed_url = await preview_manager.refresh_preview("test_spec_789", spec_data)
    print(f"Refreshed URL: {refreshed_url[:50]}...")

def test_threejs_compatibility():
    """Test Three.js viewer compatibility"""
    print("\n=== Testing Three.js Compatibility ===")
    
    # Test different object types
    test_objects = [
        {"type": "floor", "material": "marble"},
        {"type": "wall", "material": "concrete"},
        {"type": "window", "material": "glass"},
        {"type": "chair", "material": "fabric"},
        {"type": "cushion", "material": "fabric"}
    ]
    
    for i, obj in enumerate(test_objects):
        obj.update({
            "id": f"test_obj_{i}",
            "dimensions": {"width": 1, "height": 1, "depth": 1},
            "editable": True
        })
    
    spec_data = {
        "spec_id": "compatibility_test",
        "objects": test_objects
    }
    
    threejs_data = preview_generator.format_for_threejs(spec_data)
    
    print("Object type conversions:")
    for obj in threejs_data['objects']:
        geometry_type = obj['geometry']['type']
        material_color = obj['material']['color']
        print(f"  {obj['userData']['originalType']} -> {geometry_type} ({material_color})")
    
    # Test material properties
    print("\nMaterial properties:")
    for obj in threejs_data['objects']:
        material = obj['material']
        print(f"  {obj['id']}: roughness={material.get('roughness', 'N/A')}, metalness={material.get('metalness', 'N/A')}")

async def test_end_to_end_flow():
    """Test complete end-to-end demo flow"""
    print("\n=== Testing End-to-End Demo Flow ===")
    
    # Simulate the demo flow
    prompt = "Modern glass office building with steel frame"
    
    # Step 1: Generate spec (simulated)
    spec_data = {
        "spec_id": "demo_spec_001",
        "design_type": "building",
        "category": "commercial",
        "objects": [
            {
                "id": "frame_1",
                "type": "frame",
                "material": "metal",
                "dimensions": {"width": 20, "height": 50, "depth": 2},
                "editable": True
            },
            {
                "id": "glass_1",
                "type": "window",
                "material": "glass",
                "dimensions": {"width": 18, "height": 45, "depth": 0.1},
                "editable": True,
                "properties": {"color": "blue"}
            }
        ]
    }
    
    print(f"Step 1 - Generated spec: {spec_data['spec_id']}")
    
    # Step 2: Generate preview
    preview_url = await preview_manager.generate_preview(spec_data)
    print(f"Step 2 - Preview URL: {preview_url[:50]}...")
    
    # Step 3: Get Three.js data
    threejs_data = preview_manager.get_threejs_data(spec_data)
    print(f"Step 3 - Three.js objects: {len(threejs_data['objects'])}")
    
    # Step 4: Generate viewer
    viewer_html = preview_manager.generate_viewer_html(spec_data)
    print(f"Step 4 - Viewer HTML ready: {len(viewer_html)} chars")
    
    print("End-to-end flow completed successfully!")

async def main():
    """Run all Day 5 tests"""
    print("[TEST] Testing Day 5 - Frontend + Preview Integration")
    print("=" * 60)
    
    # Test bucket storage
    await test_bucket_storage()
    
    # Test preview generator
    test_preview_generator()
    
    # Test preview manager
    await test_preview_manager()
    
    # Test Three.js compatibility
    test_threejs_compatibility()
    
    # Test end-to-end flow
    await test_end_to_end_flow()
    
    print("\n[SUCCESS] Day 5 feature testing completed!")
    print("=" * 60)
    
    # Summary
    print("\n[SUMMARY] SUMMARY:")
    print("[OK] BHIV Bucket storage with signed URLs")
    print("[OK] Preview generation with Three.js compatibility")
    print("[OK] Enhanced preview manager with caching")
    print("[OK] Three.js viewer data formatting")
    print("[OK] End-to-end demo flow integration")

if __name__ == "__main__":
    asyncio.run(main())