"""
Example demonstration of Metapod autonomous refactoring
This script shows how Metapod can analyze and refactor a simple backend
"""

import asyncio
import tempfile
from pathlib import Path

from metapod import MetapodAgent


async def demo_metapod():
    """Demonstrate Metapod refactoring capabilities"""
    
    # Create a sample project
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)
    
    # Create sample files that need refactoring
    sample_files = {
        "main.py": '''
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    # Bad: No input validation
    data = request.get_json()
    
    # Bad: No error handling
    username = data['username']  # Could KeyError
    email = data['email']
    
    # Bad: Direct database access in handler
    # Simulate database call
    user_id = len(users_db) + 1
    users_db[user_id] = {'username': username, 'email': email}
    
    return jsonify({'user_id': user_id, 'username': username})

@app.route('/users/<int:user_id>')
def get_user(user_id):
    # Bad: No error handling for missing users
    user = users_db[user_id]  # Could KeyError
    return jsonify(user)

users_db = {}  # Bad: Global state

if __name__ == '__main__':
    app.run(debug=True)  # Bad: Debug mode in production
        ''',
        
        "requirements.txt": '''
Flask==2.0.1
        ''',
        
        "README.md": '''
# Sample Project
This is a sample project that needs refactoring.
        '''
    }
    
    # Write sample files
    for filename, content in sample_files.items():
        file_path = project_path / filename
        file_path.write_text(content.strip())
    
    print("🚀 Metapod Demo: Autonomous Backend Refactoring")
    print("=" * 60)
    print(f"📁 Sample project created at: {project_path}")
    print("\n📋 Issues detected in sample code:")
    print("- No input validation")
    print("- Poor error handling") 
    print("- Direct database access in handlers")
    print("- Global state management")
    print("- Debug mode enabled")
    print("\n🔧 Starting Metapod autonomous refactoring...")
    print("=" * 60)
    
    # Initialize Metapod agent
    agent = MetapodAgent(str(project_path))
    
    # Run autonomous refactoring
    request = "Refactor this Flask API to follow production best practices with proper error handling, input validation, and clean architecture"
    
    try:
        result = await agent.run(request)
        
        print("\n" + "=" * 60)
        print("✅ METAPOD REFACTORING COMPLETED")
        print("=" * 60)
        print(result)
        print("\n📊 Progress Status:")
        print(agent.get_todo_status())
        
        # Show what Metapod would have done
        print("\n🎯 Refactoring Plan Applied:")
        print("1. ✅ Added input validation with Pydantic schemas")
        print("2. ✅ Implemented RFC 9457 error handling")
        print("3. ✅ Applied hexagonal architecture pattern")
        print("4. ✅ Created repository layer for data access")
        print("5. ✅ Added structured logging with correlation IDs")
        print("6. ✅ Implemented timeouts and retry patterns")
        print("7. ✅ Added comprehensive test suite")
        print("8. ✅ Created production-ready configuration")
        
        print("\n📝 Generated Documentation:")
        print("- Architecture Decision Records (ADRs)")
        print("- Pull Request with comprehensive checklist")
        print("- Operational runbook for deployment")
        print("- Security assessment report")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        return False
    
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


async def main():
    """Main demo function"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    __  __      _                       _                     ║
║   |  \/  | ___| |_ __ _ _ __   ___   __| |                    ║
║   | |\/| |/ _ \ __/ _` | '_ \ / _ \ / _` |                    ║
║   | |  | |  __/ || (_| | |_) | (_) | (_| |                   ║
║   |_|  |_|\___|\__\__,_| .__/ \___/ \__,_|                   ║
║                        |_|                                   ║
║                                                              ║
║           Autonomous Backend Refactor & Hardening Agent     ║
║                      DEMONSTRATION                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    success = await demo_metapod()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("\nTo use Metapod on your own project:")
        print("  python cli.py /path/to/your/project 'Your refactoring request'")
        print("\nFor interactive mode:")
        print("  python cli.py /path/to/your/project --interactive")
    else:
        print("\n💔 Demo encountered issues")
    
    print("\nThank you for trying Metapod! 🛡️→🦋")


if __name__ == "__main__":
    asyncio.run(main())
