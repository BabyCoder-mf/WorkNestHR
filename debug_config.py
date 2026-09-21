# debug_config.py
import sys
import os

print("=== Current Working Directory ===")
print(f"Working dir: {os.getcwd()}")

print("\n=== Python Path ===")
for path in sys.path:
    print(f"  {path}")

print("\n=== Files in Current Directory ===")
for file in os.listdir('.'):
    print(f"  {file}")

print("\n=== Testing config import ===")

try:
    # Test 1: Import the module
    import config
    print("✅ config module imported")

    # Test 2: Check what's in the module
    print("Contents of config module:")
    for item in dir(config):
        if not item.startswith('_'):
            print(f"  - {item}: {getattr(config, item)}")

    # Test 3: Try to access Config class
    if hasattr(config, 'Config'):
        print("✅ Config class found!")
        cfg = config.Config()
        print(f"SECRET_KEY: {cfg.SECRET_KEY}")
        print(f"DB URI: {cfg.SQLALCHEMY_DATABASE_URI}")
    else:
        print("❌ Config class NOT found in config module")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()