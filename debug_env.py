#!/usr/bin/env python3
"""
Debug script to help diagnose API key loading issues with edge-assistant
"""
import os
from pathlib import Path
from edge_assistant.engine import Engine

def main():
    print("=== Edge Assistant API Key Diagnostics ===\n")
    
    # Show current directory
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")
    
    # Check environment before Engine creation
    print(f"OPENAI_API_KEY in environment (before): {'Yes' if 'OPENAI_API_KEY' in os.environ else 'No'}")
    if 'OPENAI_API_KEY' in os.environ:
        key_value = os.environ['OPENAI_API_KEY']
        print(f"  Value: {key_value[:10]}{'*' * (len(key_value) - 10) if len(key_value) > 10 else key_value}")
    
    # Show .env file search path
    print(f"\n.env file search:")
    env_path = cwd / ".env"
    print(f"  {cwd}/.env exists: {env_path.exists()}")
    if env_path.exists():
        try:
            content = env_path.read_text().strip()
            lines = content.split('\n')
            for line in lines:
                if line.startswith('OPENAI_API_KEY'):
                    key_part = line.split('=', 1)[1] if '=' in line else ''
                    key_part = key_part.strip('"').strip("'")  # Remove quotes
                    print(f"    Found: OPENAI_API_KEY={key_part[:10]}{'*' * (len(key_part) - 10) if len(key_part) > 10 else key_part}")
        except Exception as e:
            print(f"    Error reading .env: {e}")
    
    # Check parent directories
    for parent in cwd.parents:
        env_path = parent / ".env"
        if env_path.exists():
            print(f"  {parent}/.env exists: True")
            try:
                content = env_path.read_text().strip()
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('OPENAI_API_KEY'):
                        key_part = line.split('=', 1)[1] if '=' in line else ''
                        key_part = key_part.strip('"').strip("'")
                        print(f"    Found: OPENAI_API_KEY={key_part[:10]}{'*' * (len(key_part) - 10) if len(key_part) > 10 else key_part}")
            except Exception as e:
                print(f"    Error reading .env: {e}")
        
        # Stop at git root or pyproject.toml (same logic as Engine)
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            print(f"  Stopping search at {parent} (found .git or pyproject.toml)")
            break
    
    # Create engine and check after
    print(f"\nCreating Engine instance...")
    try:
        engine = Engine()
        print("Engine created successfully")
    except Exception as e:
        print(f"Error creating Engine: {e}")
        return
    
    # Check environment after Engine creation
    print(f"OPENAI_API_KEY in environment (after): {'Yes' if 'OPENAI_API_KEY' in os.environ else 'No'}")
    if 'OPENAI_API_KEY' in os.environ:
        key_value = os.environ['OPENAI_API_KEY']
        print(f"  Value: {key_value[:10]}{'*' * (len(key_value) - 10) if len(key_value) > 10 else key_value}")
        
        # Basic validation
        if not key_value.startswith('sk-'):
            print("  ⚠️  Warning: API key doesn't start with 'sk-'")
        elif len(key_value) < 20:
            print("  ⚠️  Warning: API key seems too short")
        else:
            print("  ✓ API key format looks reasonable")
    
    print(f"\n=== Summary ===")
    if 'OPENAI_API_KEY' not in os.environ:
        print("❌ No API key found. Please ensure you have a .env file with OPENAI_API_KEY=your-key")
    else:
        key = os.environ['OPENAI_API_KEY']
        if not key.startswith('sk-'):
            print("❌ API key format is incorrect (should start with 'sk-')")
        elif len(key) < 20:
            print("❌ API key appears to be too short")
        else:
            print("✓ API key found and format looks correct")
            print("  If you're still getting errors, the key might be invalid or expired.")

if __name__ == "__main__":
    main()