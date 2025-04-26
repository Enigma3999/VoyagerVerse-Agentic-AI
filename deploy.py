import os
import subprocess
import webbrowser
import time
import sys

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pyngrok
        return True
    except ImportError:
        print("Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
        return True

def start_fastapi_server():
    """Start the FastAPI server in the background"""
    print("Starting VoyagerVerse server...")
    # Start the server as a background process
    if os.name == 'nt':  # Windows
        process = subprocess.Popen([sys.executable, "main_v2.py"], 
                                  creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Linux/Mac
        process = subprocess.Popen([sys.executable, "main_v2.py"], 
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    
    # Give the server a moment to start
    time.sleep(3)
    return process

def start_ngrok_tunnel():
    """Create an ngrok tunnel to the FastAPI server"""
    from pyngrok import ngrok, conf
    
    # Set ngrok auth token if available
    token = os.environ.get("NGROK_AUTH_TOKEN")
    if token:
        conf.get_default().auth_token = token
    
    # Start ngrok tunnel
    print("Creating secure tunnel for sharing...")
    http_tunnel = ngrok.connect(8000)
    public_url = http_tunnel.public_url
    
    print("\n" + "=" * 70)
    print(f"🚀 VoyagerVerse is now available at: {public_url}")
    print("=" * 70)
    print("\nShare this URL with others to access your VoyagerVerse prototype!")
    print("\nAvailable demo pages:")
    print(f"- Simple Chat Demo: {public_url}/simple-chat")
    print(f"- Simple Agent UI: {public_url}/simple-agent")
    print(f"- Conversation Demo: {public_url}/conversation-demo")
    print(f"- Agent Calling Demo: {public_url}/agent-calling-demo")
    print("\nPress Ctrl+C to stop the server when you're done.")
    
    return public_url

def open_demo_pages(public_url):
    """Open the demo pages in the default browser"""
    print("\nOpening demo pages in your browser...")
    webbrowser.open(f"{public_url}/simple-chat")
    time.sleep(1)
    webbrowser.open(f"{public_url}/simple-agent")

def main():
    """Main function to deploy VoyagerVerse"""
    print("\n🌟 VoyagerVerse Deployment Tool 🌟\n")
    
    if not check_dependencies():
        print("Failed to install required dependencies. Please try again.")
        return
    
    server_process = start_fastapi_server()
    
    try:
        public_url = start_ngrok_tunnel()
        
        # Ask if user wants to open demo pages
        open_browser = input("\nWould you like to open the demo pages in your browser? (y/n): ")
        if open_browser.lower() == 'y':
            open_demo_pages(public_url)
        
        # Keep the script running until interrupted
        print("\nPress Ctrl+C to stop the server and close the tunnel.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down VoyagerVerse...")
    finally:
        # Clean up
        if 'ngrok' in sys.modules:
            from pyngrok import ngrok
            ngrok.kill()
        
        if server_process:
            server_process.terminate()
        
        print("VoyagerVerse has been shut down. Thank you for using the deployment tool!")

if __name__ == "__main__":
    main()
