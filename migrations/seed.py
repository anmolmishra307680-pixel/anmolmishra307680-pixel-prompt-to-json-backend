"""Database Seed Script"""
import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.database import Database

def seed_database():
    try:
        db = Database()
        session = db.get_session()
        
        from data.models import Specs
        
        seed_spec = Specs(
            spec_id="spec_seed",
            user_id="u0", 
            prompt="seed",
            spec_json={},
            agent_type="MainAgent",
            created_at=datetime.now(timezone.utc)
        )
        
        existing = session.query(Specs).filter_by(spec_id="spec_seed").first()
        if not existing:
            session.add(seed_spec)
            session.commit()
            print("✅ Seed data added")
        else:
            print("⏭️ Seed data already exists")
            
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        return False

if __name__ == "__main__":
    seed_database()