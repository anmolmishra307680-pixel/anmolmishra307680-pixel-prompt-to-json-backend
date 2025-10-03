#!/usr/bin/env python3
"""
Database Seed Script
Populates initial data for development and testing
"""
import sqlite3
import json
from datetime import datetime, timedelta
import uuid
import random
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def seed_database():
    """Seed the database with initial data"""
    conn = sqlite3.connect('prompt_to_json.db')
    cursor = conn.cursor()
    
    # Sample design specs
    sample_specs = [
        {
            "id": str(uuid.uuid4()),
            "prompt": "Modern office building with solar panels",
            "design_type": "building",
            "specification": json.dumps({
                "materials": [{"type": "steel", "grade": "A36"}],
                "dimensions": {"length": 50, "width": 30, "height": 20},
                "features": ["solar_panels", "energy_efficient"]
            }),
            "created_at": datetime.now().isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "prompt": "Electric vehicle with 300-mile range",
            "design_type": "vehicle",
            "specification": json.dumps({
                "materials": [{"type": "aluminum", "grade": "6061-T6"}],
                "dimensions": {"length": 4.5, "width": 1.8, "height": 1.4},
                "performance": {"range": 300, "power": 250}
            }),
            "created_at": datetime.now().isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "prompt": "Smart home IoT sensor with WiFi",
            "design_type": "electronics",
            "specification": json.dumps({
                "materials": [{"type": "plastic", "grade": "ABS"}],
                "dimensions": {"length": 0.1, "width": 0.08, "height": 0.03},
                "features": ["wifi", "battery_powered", "weatherproof"]
            }),
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specs (
            id TEXT PRIMARY KEY,
            prompt TEXT NOT NULL,
            design_type TEXT,
            specification TEXT,
            created_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id TEXT PRIMARY KEY,
            spec_id TEXT,
            overall_score REAL,
            criteria_scores TEXT,
            created_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iteration_logs (
            id TEXT PRIMARY KEY,
            spec_id TEXT,
            iteration_count INTEGER,
            feedback TEXT,
            improvements TEXT,
            created_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mobile_sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            platform TEXT,
            device_info TEXT,
            session_data TEXT,
            created_at TEXT,
            last_active TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vr_experiences (
            id TEXT PRIMARY KEY,
            spec_id TEXT,
            vr_platform TEXT,
            immersion_level TEXT,
            scene_config TEXT,
            export_formats TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cost_tracking (
            id TEXT PRIMARY KEY,
            operation_type TEXT,
            compute_type TEXT,
            tokens_used INTEGER,
            cost_usd REAL,
            duration_ms INTEGER,
            timestamp TEXT
        )
    """)
    
    # Insert sample specs
    for spec in sample_specs:
        cursor.execute("""
            INSERT OR REPLACE INTO specs 
            (id, prompt, design_type, specification, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (spec["id"], spec["prompt"], spec["design_type"], 
               spec["specification"], spec["created_at"]))
    
    # Sample evaluations
    sample_evaluations = [
        {
            "id": str(uuid.uuid4()),
            "spec_id": sample_specs[0]["id"],
            "overall_score": 8.5,
            "criteria_scores": json.dumps({
                "feasibility": 9.0,
                "sustainability": 8.0,
                "cost_effectiveness": 8.5,
                "innovation": 7.5,
                "market_viability": 8.8
            }),
            "created_at": datetime.now().isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "spec_id": sample_specs[1]["id"],
            "overall_score": 9.2,
            "criteria_scores": json.dumps({
                "feasibility": 9.5,
                "sustainability": 9.8,
                "cost_effectiveness": 8.0,
                "innovation": 9.5,
                "market_viability": 9.2
            }),
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # Insert sample evaluations
    for eval_data in sample_evaluations:
        cursor.execute("""
            INSERT OR REPLACE INTO evaluations
            (id, spec_id, overall_score, criteria_scores, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (eval_data["id"], eval_data["spec_id"], eval_data["overall_score"],
               eval_data["criteria_scores"], eval_data["created_at"]))
    
    # Sample iteration logs
    sample_iterations = [
        {
            "id": str(uuid.uuid4()),
            "spec_id": sample_specs[0]["id"],
            "iteration_count": 3,
            "feedback": "Make it more sustainable",
            "improvements": json.dumps([
                "Added recycled materials (+20% sustainability)",
                "Improved energy efficiency (+15%)",
                "Reduced construction waste (-30%)"
            ]),
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # Insert sample iterations
    for iter_data in sample_iterations:
        cursor.execute("""
            INSERT OR REPLACE INTO iteration_logs
            (id, spec_id, iteration_count, feedback, improvements, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (iter_data["id"], iter_data["spec_id"], iter_data["iteration_count"],
               iter_data["feedback"], iter_data["improvements"], iter_data["created_at"]))
    
    # Sample mobile sessions
    sample_mobile_sessions = [
        {
            "id": str(uuid.uuid4()),
            "user_id": "user_001",
            "platform": "react-native",
            "device_info": json.dumps({
                "os": "iOS",
                "version": "16.0",
                "device": "iPhone 14"
            }),
            "session_data": json.dumps({
                "specs_generated": 5,
                "last_prompt": "Smart doorbell with camera"
            }),
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat()
        }
    ]
    
    # Insert mobile sessions
    for session in sample_mobile_sessions:
        cursor.execute("""
            INSERT OR REPLACE INTO mobile_sessions
            (id, user_id, platform, device_info, session_data, created_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session["id"], session["user_id"], session["platform"],
               session["device_info"], session["session_data"], 
               session["created_at"], session["last_active"]))
    
    # Sample VR experiences
    sample_vr_experiences = [
        {
            "id": str(uuid.uuid4()),
            "spec_id": sample_specs[0]["id"],
            "vr_platform": "oculus",
            "immersion_level": "full",
            "scene_config": json.dumps({
                "lighting": "natural",
                "environment": "studio",
                "interaction_methods": ["hand_tracking", "controllers"]
            }),
            "export_formats": json.dumps(["unity", "webxr"]),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    ]
    
    # Insert VR experiences
    for vr_exp in sample_vr_experiences:
        cursor.execute("""
            INSERT OR REPLACE INTO vr_experiences
            (id, spec_id, vr_platform, immersion_level, scene_config, export_formats, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (vr_exp["id"], vr_exp["spec_id"], vr_exp["vr_platform"],
               vr_exp["immersion_level"], vr_exp["scene_config"], 
               vr_exp["export_formats"], vr_exp["created_at"], vr_exp["updated_at"]))
    
    # Sample cost tracking data
    sample_costs = []
    for i in range(10):
        sample_costs.append({
            "id": str(uuid.uuid4()),
            "operation_type": random.choice(["generate", "evaluate", "iterate"]),
            "compute_type": random.choice(["local_rtx3060", "yotta_cloud"]),
            "tokens_used": random.randint(100, 2000),
            "cost_usd": round(random.uniform(0.001, 0.05), 4),
            "duration_ms": random.randint(500, 5000),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat()
        })
    
    # Insert cost tracking
    for cost in sample_costs:
        cursor.execute("""
            INSERT OR REPLACE INTO cost_tracking
            (id, operation_type, compute_type, tokens_used, cost_usd, duration_ms, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (cost["id"], cost["operation_type"], cost["compute_type"],
               cost["tokens_used"], cost["cost_usd"], cost["duration_ms"], cost["timestamp"]))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Seeded database with:")
    print(f"   - {len(sample_specs)} design specs")
    print(f"   - {len(sample_evaluations)} evaluations")
    print(f"   - {len(sample_iterations)} iteration logs")
    print(f"   - {len(sample_mobile_sessions)} mobile sessions")
    print(f"   - {len(sample_vr_experiences)} VR experiences")
    print(f"   - {len(sample_costs)} cost tracking records")
    return True

if __name__ == "__main__":
    seed_database()