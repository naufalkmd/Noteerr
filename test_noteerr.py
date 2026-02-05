"""
Test script to verify Noteerr installation and functionality.
Run this after installing: python test_noteerr.py
"""

import os
import sys
import subprocess


def run_command(cmd):
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def test_installation():
    """Test if noteerr is installed."""
    print("🔍 Testing Noteerr installation...")
    
    success, stdout, stderr = run_command("noteerr --version")
    
    if success:
        print("✅ Noteerr is installed correctly!")
        print(f"   Version: {stdout.strip()}")
        return True
    else:
        print("❌ Noteerr is not installed or not in PATH")
        print(f"   Error: {stderr}")
        return False


def test_basic_commands():
    """Test basic Noteerr commands."""
    print("\n🧪 Testing basic commands...\n")
    
    tests = [
        ("noteerr list", "List command"),
        ("noteerr stats", "Stats command"),
        ("noteerr --help", "Help command"),
    ]
    
    passed = 0
    failed = 0
    
    for cmd, description in tests:
        print(f"Testing: {description}")
        success, stdout, stderr = run_command(cmd)
        
        if success or "No errors logged yet" in stdout or "No errors" in stdout:
            print(f"  ✅ {description} works!")
            passed += 1
        else:
            print(f"  ❌ {description} failed")
            print(f"     Error: {stderr}")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_save_and_retrieve():
    """Test saving and retrieving an error."""
    print("\n🧪 Testing save and retrieve functionality...\n")
    
    # Save a test error
    print("1. Saving a test error...")
    cmd = 'noteerr save "test error from installation script" --command "test-command" --error "test error message" --tags test,installation'
    success, stdout, stderr = run_command(cmd)
    
    if not success:
        print(f"  ❌ Failed to save error: {stderr}")
        return False
    
    print("  ✅ Error saved successfully!")
    
    # List errors
    print("2. Listing errors...")
    success, stdout, stderr = run_command("noteerr list")
    
    if success and "test-command" in stdout:
        print("  ✅ Error appears in list!")
    else:
        print("  ❌ Error not found in list")
        return False
    
    # Search for error
    print("3. Searching for error...")
    success, stdout, stderr = run_command("noteerr search test")
    
    if success and "test-command" in stdout:
        print("  ✅ Error found via search!")
    else:
        print("  ❌ Search failed")
        return False
    
    print("\n✅ All save/retrieve tests passed!")
    return True


def check_data_directory():
    """Check if data directory was created."""
    print("\n📁 Checking data directory...")
    
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, ".noteerr")
    data_file = os.path.join(data_dir, "errors.json")
    
    if os.path.exists(data_dir):
        print(f"  ✅ Data directory exists: {data_dir}")
    else:
        print(f"  ℹ️  Data directory will be created on first use")
    
    if os.path.exists(data_file):
        print(f"  ✅ Data file exists: {data_file}")
        return True
    else:
        print(f"  ℹ️  Data file will be created on first error save")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 Noteerr Installation Test Script")
    print("=" * 60)
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed. Please install Noteerr first:")
        print("   pip install -e .")
        sys.exit(1)
    
    # Test basic commands
    if not test_basic_commands():
        print("\n⚠️  Some basic commands failed")
    
    # Check data directory
    check_data_directory()
    
    # Test save and retrieve
    test_save_and_retrieve()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("=" * 60)
    print("\n📚 Next steps:")
    print("   1. Try: noteerr list")
    print("   2. Try: noteerr stats")
    print("   3. Try: noteerr search test")
    print("   4. Read EXAMPLES.md for more usage examples")
    print("   5. Set up shell integration (see README.md)")
    print("\n💡 Tip: Run a failing command and immediately type:")
    print("   noteerr save \"your note about the fix\"")


if __name__ == "__main__":
    main()
