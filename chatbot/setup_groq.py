#!/usr/bin/env python3
"""
Groq Setup Script
Helps users set up Groq API and test the configuration
"""

import os
import sys
import asyncio
from groq_service import GroqService
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def check_api_key():
    """Check if Groq API key is configured."""
    print("🔍 Checking Groq API key configuration...")
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        print("✅ Groq API key found in environment variables")
        return True, api_key
    else:
        print("❌ Groq API key not found")
        return False, None


def setup_api_key():
    """Guide user through API key setup."""
    print("\n📋 Setting up Groq API key:")
    print("1. Go to https://console.groq.com/")
    print("2. Sign up for a free account")
    print("3. Navigate to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the API key")
    
    print("\n🔑 Please enter your Groq API key: ", end="")
    api_key = input().strip()
    
    if not api_key:
        print("❌ No API key provided")
        return None
    
    # Test the API key
    print("\n🧪 Testing API key...")
    service = GroqService(api_key=api_key)
    
    if service.is_configured():
        print("✅ API key is valid")
        
        # Show how to set environment variable
        print("\n💡 To make this permanent, set the environment variable:")
        print(f"   Windows: set GROQ_API_KEY={api_key}")
        print(f"   Linux/Mac: export GROQ_API_KEY={api_key}")
        print("   Or add it to your .env file")
        
        return api_key
    else:
        print("❌ API key validation failed")
        return None


async def test_groq_service(api_key=None):
    """Test the Groq service with a simple query."""
    print("\n🧪 Testing Groq service...")
    
    try:
        service = GroqService(api_key=api_key)
        
        if not service.is_configured():
            print("❌ Groq service is not properly configured")
            return False
        
        # Test with a simple healthcare query
        test_message = "Hello, can you help me with patient information?"
        result = await service.generate_response(test_message)
        
        if result and result.get('response'):
            print("✅ Groq service test successful")
            print(f"🤖 Model used: {result.get('model_used', 'Unknown')}")
            print(f"📝 Sample response: {result['response'][:100]}...")
            return True
        else:
            print("❌ Groq service test failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Groq service: {e}")
        return False


def show_available_models():
    """Show available Groq models."""
    print("\n🧠 Available Groq models:")
    service = GroqService()
    models = service.get_available_models()
    
    for i, model in enumerate(models, 1):
        if model == "llama3-8b-8192":
            print(f"   {i}. {model} (Default - Fast and efficient)")
        elif model == "llama3-70b-4096":
            print(f"   {i}. {model} (More capable, slower)")
        elif model == "mixtral-8x7b-32768":
            print(f"   {i}. {model} (Good balance)")
        else:
            print(f"   {i}. {model}")


async def main():
    """Main setup function."""
    print("🏥 Healthcare Chatbot - Groq Setup")
    print("=" * 50)
    
    # Step 1: Check API key
    has_key, api_key = check_api_key()
    
    if not has_key:
        print("\n🤔 Would you like to set up your Groq API key now? (y/n): ", end="")
        response = input().lower().strip()
        
        if response in ['y', 'yes']:
            api_key = setup_api_key()
            if not api_key:
                print("\n❌ Setup failed. Please try again later.")
                sys.exit(1)
        else:
            print("\n⚠️  Skipping API key setup. The chatbot may not work properly.")
            print("You can run this script again later to set up the API key.")
            sys.exit(0)
    
    # Step 2: Test the service
    test_success = await test_groq_service(api_key)
    
    if test_success:
        print("\n🎉 Setup completed successfully!")
        
        # Show available models
        show_available_models()
        
        print("\n📋 Next steps:")
        print("1. Make sure your MCP server is configured (check config.py)")
        print("2. Start the chatbot: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        
        print("\n💡 Tips:")
        print("- Groq is much faster than local LLMs")
        print("- The chatbot uses natural language processing")
        print("- Ask questions like 'find patients named John' or 'show me patient list'")
        print("- Type 'help' for available commands")
        
        print("\n🚀 Advantages of Groq:")
        print("- ⚡ Ultra-fast inference (sub-second responses)")
        print("- 🆓 Free tier available")
        print("- 🧠 Multiple model options")
        print("- 🔒 Secure API access")
        
    else:
        print("\n❌ Setup completed with issues. The chatbot may not work properly.")
        print("Please check the error messages above and try again.")
        
        print("\n🔧 Troubleshooting:")
        print("- Verify your API key is correct")
        print("- Check your internet connection")
        print("- Make sure you have Groq API access")


def create_env_file(api_key):
    """Create a .env file with the API key."""
    try:
        with open('.env', 'w') as f:
            f.write(f"GROQ_API_KEY={api_key}\n")
        print("✅ Created .env file with API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
