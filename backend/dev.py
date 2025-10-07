#!/usr/bin/env python3
"""
Development server script for the backend.
Equivalent to npm run dev for the frontend.
"""

import subprocess
import sys
import os

def main():
    """Run the development server with auto-reload."""
    try:
        # Change to backend directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run uvicorn with reload
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ]
        
        print("Starting backend development server...")
        print("Backend will be available at: http://localhost:8000")
        print("Press Ctrl+C to stop")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nShutting down development server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()