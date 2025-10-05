#!/usr/bin/env python3
"""Script to generate OpenAPI client from the FastAPI service."""

import json
import subprocess
import sys
import time
from pathlib import Path

import requests
import uvicorn
from multiprocessing import Process


def start_service():
    """Start the FastAPI service."""
    import sys
    sys.path.append('src')
    uvicorn.run(
        "mail_client_services.src.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="error"
    )


def generate_openapi_spec():
    """Generate OpenAPI spec from running service."""
    print("Fetching OpenAPI spec from service...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/openapi.json", timeout=10)
        response.raise_for_status()
        
        # Save the OpenAPI spec
        spec_path = Path("openapi.json")
        with open(spec_path, "w") as f:
            json.dump(response.json(), f, indent=2)
        
        print(f"OpenAPI spec saved to {spec_path}")
        return spec_path
        
    except Exception as e:
        print(f"Failed to fetch OpenAPI spec: {e}")
        return None


def generate_client(spec_path: Path):
    """Generate Python client using openapi-python-client."""
    print("🔧 Generating Python client...")
    
    try:
        # Remove existing generated client
        generated_path = Path("src/mail_client_generated")
        if generated_path.exists():
            import shutil
            shutil.rmtree(generated_path)
        
        # Generate the client
        cmd = [
            sys.executable, "-m", "openapi_python_client", "generate",
            "--path", str(spec_path),
            "--output-path", "src",
            "--package-name", "mail_client_generated"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Client generated successfully!")
            print(f"📁 Generated client at: src/mail_client_generated/")
            return True
        else:
            print(f"❌ Client generation failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating client: {e}")
        return False


def main():
    """Main function to generate the client."""
    print("🚀 Generating OpenAPI Python Client")
    print("=" * 40)
    
    # Start the service in a separate process
    print("🔄 Starting FastAPI service...")
    service_process = Process(target=start_service)
    service_process.start()
    
    try:
        # Wait for service to start
        time.sleep(3)
        
        # Generate OpenAPI spec
        spec_path = generate_openapi_spec()
        if not spec_path:
            return False
        
        # Generate client
        success = generate_client(spec_path)
        
        if success:
            print("\n🎉 Client generation completed!")
            print("💡 Next steps:")
            print("   1. Check the generated client in src/mail_client_generated/")
            print("   2. Create a wrapper to implement the Client interface")
            print("   3. Replace the manual adapter")
        
        return success
        
    finally:
        # Clean up
        service_process.terminate()
        service_process.join(timeout=5)
        if service_process.is_alive():
            service_process.kill()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)