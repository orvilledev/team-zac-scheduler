"""Check if port 5000 is available and test server startup"""
import socket
import sys

def check_port(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        return True
    except OSError:
        return False

if __name__ == '__main__':
    port = 5000
    print(f"Checking if port {port} is available...")
    
    if check_port(port):
        print(f"✓ Port {port} is available")
    else:
        print(f"✗ Port {port} is already in use!")
        print("Please stop any application using this port.")
        sys.exit(1)
    
    print("\nAttempting to start Flask app...")
    try:
        from app import app
        print("App imported successfully")
        
        # Try to create a test client
        with app.app_context():
            print("App context created successfully")
        
        print("\n✓ Everything looks good! You can now run: py app.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

