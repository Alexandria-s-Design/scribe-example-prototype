"""Test Cell Collective authentication"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from cell_collective_api import CellCollectiveAPI

# Initialize API
api = CellCollectiveAPI()

# Set token (fresh from user)
token = "s%3ADTibDdbTzQEnkGCGKlekekOSGL5h_x39.Rm1AMOVg0rh2VxGs3XYdIEf1PvpfOhi9PEHtqQsRG2Q"
api.set_token(token)

print("\n" + "="*60)
print("Testing Cell Collective Authentication")
print("="*60)

# Test 1: Get profile
print("\n[TEST 1] Getting user profile...")
profile = api.get_profile()
if profile:
    print(f"SUCCESS - Profile loaded!")
    print(f"  User data: {profile.get('data', {})}")
else:
    print("X Failed to get profile (401 unauthorized)")

# Test 2: Get model
print("\n[TEST 2] Getting model 298697...")
model = api.get_model(298697, version=1, slim=False)
if model:
    components = model.get('externalComponentSet', [])
    relationships = model.get('relationshipSet', [])
    print(f"SUCCESS - Model loaded!")
    print(f"  Name: {model.get('name', 'Unknown')}")
    print(f"  Components: {len(components)}")
    print(f"  Relationships: {len(relationships)}")

    if len(components) > 0:
        print(f"\n  First 5 components:")
        for comp in components[:5]:
            print(f"    - {comp.get('name', comp.get('externalName', 'Unknown'))}")
else:
    print("X Failed to get model")

print("\n" + "="*60)
