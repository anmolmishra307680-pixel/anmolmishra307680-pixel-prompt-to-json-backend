"""Test database migrations"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import models

def test_migration_tables_exist():
    """Test that all required tables exist in metadata"""
    table_names = [t.name for t in models.Base.metadata.sorted_tables]
    
    # Check that required tables exist
    assert "specs" in table_names, "specs table not found in metadata"
    assert "evals" in table_names, "evals table not found in metadata" 
    assert "feedback_logs" in table_names, "feedback_logs table not found in metadata"
    assert "hidg_logs" in table_names, "hidg_logs table not found in metadata"
    assert "iteration_logs" in table_names, "iteration_logs table not found in metadata"
    
    print(f"Found tables: {table_names}")
    print("All migration tables verified successfully")

def test_table_structure():
    """Test basic table structure"""
    # Test specs table
    specs_table = models.Base.metadata.tables['specs']
    assert 'id' in specs_table.columns
    assert 'prompt' in specs_table.columns
    assert 'spec_data' in specs_table.columns
    
    # Test evals table  
    evals_table = models.Base.metadata.tables['evals']
    assert 'id' in evals_table.columns
    assert 'spec_id' in evals_table.columns
    assert 'eval_data' in evals_table.columns
    assert 'score' in evals_table.columns
    
    print("Table structures verified successfully")

if __name__ == "__main__":
    test_migration_tables_exist()
    test_table_structure()