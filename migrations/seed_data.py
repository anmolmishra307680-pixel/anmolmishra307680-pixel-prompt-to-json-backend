"""Seed sample data for testing"""

import json
from pathlib import Path
from src.data.database import Database
from src.schemas.spec_schema import Spec, ObjectSpec, SceneSpec

def seed_sample_spec():
    """Seed one sample spec for testing"""
    
    # Create sample spec
    sample_spec = Spec(
        spec_id="sample_office_001",
        objects=[
            ObjectSpec(
                id="floor_001",
                type="floor",
                material="wood",
                editable=True,
                properties={
                    "finish": "matte",
                    "color": "brown",
                    "area": 100.0
                }
            ),
            ObjectSpec(
                id="wall_001", 
                type="wall",
                material="drywall",
                editable=True,
                properties={
                    "color": "white",
                    "height": 3.0,
                    "thickness": 0.15
                }
            ),
            ObjectSpec(
                id="desk_001",
                type="desk", 
                material="wood",
                editable=True,
                properties={
                    "width": 1.5,
                    "depth": 0.8,
                    "height": 0.75,
                    "color": "oak"
                }
            ),
            ObjectSpec(
                id="chair_001",
                type="chair",
                material="fabric",
                editable=True,
                properties={
                    "color": "blue",
                    "cushion_type": "memory_foam",
                    "adjustable": True
                }
            )
        ],
        scene=SceneSpec(
            environment="office",
            lighting="fluorescent", 
            scale=1.0,
            background="neutral"
        ),
        design_type="building",
        metadata={
            "created_by": "seed_script",
            "purpose": "testing",
            "room_type": "office"
        }
    )
    
    try:
        # Try database first
        db = Database()
        spec_id = db.save_spec(
            prompt="Modern office space with wooden floors",
            spec_data=sample_spec.dict(),
            agent_type="SeedScript"
        )
        print(f"✅ Seeded sample spec to database: {spec_id}")
        
    except Exception as e:
        print(f"⚠️ Database seeding failed: {e}")
        
        # Fallback to file storage
        specs_dir = Path("spec_outputs")
        specs_dir.mkdir(exist_ok=True)
        
        spec_file = specs_dir / f"{sample_spec.spec_id}.json"
        with open(spec_file, 'w') as f:
            json.dump(sample_spec.dict(), f, indent=2)
        
        print(f"✅ Seeded sample spec to file: {spec_file}")
    
    return sample_spec

if __name__ == "__main__":
    print("🌱 Seeding sample data...")
    sample_spec = seed_sample_spec()
    print(f"📋 Sample spec ID: {sample_spec.spec_id}")
    print("✨ Seeding complete!")