#!/usr/bin/env python3
"""
Test script for DataTables implementation
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Logic.Data.DataTables import DataTables, DataType
from Logic.Data.Specific.LocationData import LocationData

def test_datatables_loading():
    """Test that DataTables loads correctly"""
    print("Testing DataTables loading...")
    
    # Test if tables are loaded
    if DataTables.TABLES:
        print(f"✓ DataTables loaded successfully")
        print(f"✓ Number of tables: {len(DataTables.TABLES._data_tables)}")
    else:
        print("✗ DataTables failed to load")
        return False
    
    return True

def test_location_data():
    """Test LocationData specific functionality"""
    print("\nTesting LocationData...")
    
    location_table = DataTables.get(DataType.LOCATION)
    if not location_table:
        print("✗ Location table not found")
        return False
    
    print(f"✓ Location table found with {location_table.count()} entries")
    
    # Test getting location by name
    test_locations = ["Wanted1", "Wanted3", "Wanted4"]
    
    for location_name in test_locations:
        location_data = location_table.get_data(location_name)
        if location_data and isinstance(location_data, LocationData):
            print(f"✓ Found location '{location_name}': {location_data}")
            print(f"  Game Mode: {location_data.game_mode}")
            print(f"  Allowed Maps: {location_data.allowed_maps}")
            print(f"  Enabled: {location_data.is_enabled()}")
        else:
            print(f"✗ Location '{location_name}' not found")
    
    return True

def test_data_retrieval_methods():
    """Test various data retrieval methods"""
    print("\nTesting data retrieval methods...")
    
    # Test get_data_with_name
    location = DataTables.get_data_with_name(DataType.LOCATION, "Wanted1")
    if location:
        print(f"✓ get_data_with_name works: {location.name}")
    else:
        print("✗ get_data_with_name failed")
    
    # Test get_instance_id
    instance_id = DataTables.get_instance_id(DataType.LOCATION, "Wanted1")
    if instance_id >= 0:
        print(f"✓ get_instance_id works: {instance_id}")
    else:
        print("✗ get_instance_id failed")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("DataTables Test Suite")
    print("=" * 50)
    
    success = True
    success &= test_datatables_loading()
    success &= test_location_data()
    success &= test_data_retrieval_methods()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    print("=" * 50)
