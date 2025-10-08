"""Demo script for backend integration testing"""

from src.api_client import APIClient
import json

def main():
    print("🚀 BHIV Backend Integration Demo")
    print("=" * 40)
    
    # Initialize client
    client = APIClient(
        base_url="http://localhost:8000",
        api_key="bhiv-secret-key-2024"
    )
    
    try:
        # Step 1: Login
        print("\n1️⃣ Authenticating...")
        auth_result = client.login("admin", "bhiv2024")
        print(f"✅ Logged in as: {auth_result['user_id']}")
        
        # Step 2: Generate specification
        print("\n2️⃣ Generating specification...")
        spec = client.generate(
            prompt="Test room with modern furniture",
            context={"style": "modern", "room_type": "office"}
        )
        spec_id = spec["spec_id"]
        print(f"✅ Generated spec: {spec_id}")
        print(f"📋 Objects: {len(spec['spec_json']['objects'])}")
        
        # Step 3: Switch material
        print("\n3️⃣ Switching floor material...")
        switched = client.switch(
            spec_id=spec_id,
            target={"object_id": "obj_001"},
            update={"material": "marble"},
            note="Changed to marble for elegance"
        )
        print(f"✅ Material switched: {switched['changed']['before']} → {switched['changed']['after']}")
        
        # Step 4: Run compliance case
        print("\n4️⃣ Running compliance check...")
        case = client.compliance_run_case({
            "case_id": "demo_case_001",
            "project_id": "demo_project",
            "spec_data": spec["spec_json"],
            "compliance_rules": ["fire_safety", "accessibility"]
        })
        print(f"✅ Compliance status: {case['result'].get('status', 'completed')}")
        
        # Step 5: Core pipeline
        print("\n5️⃣ Running core pipeline...")
        pipeline = client.core_run(
            prompt="Enhanced office space",
            iterations=2,
            compliance_check=True
        )
        print(f"✅ Pipeline completed in {pipeline['processing_time']:.2f}s")
        
        # Step 6: Display preview URLs
        print("\n6️⃣ Preview URLs:")
        print(f"🎨 Original: {spec.get('preview_url', 'N/A')}")
        print(f"🔄 Switched: {switched.get('preview_url', 'N/A')}")
        
        # Summary
        print("\n" + "=" * 40)
        print("✨ Demo completed successfully!")
        print(f"📊 Spec ID: {spec_id}")
        print(f"🏗️ Pipeline ID: {pipeline['pipeline_id']}")
        print(f"⚡ Total processing: {pipeline['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()