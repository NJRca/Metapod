"""
VSCode Agent Integration for Metapod
Allows Metapod to be registered and used as a selectable agent within VSCode
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

from metapod import MetapodAgent
from config import DEFAULT_CONFIG


class VSCodeAgentAdapter:
    """
    Adapter that makes Metapod compatible with VSCode agent protocols
    """
    
    def __init__(self):
        self.agent_id = "metapod-autonomous-refactor"
        self.display_name = "Metapod - Autonomous Backend Refactor Agent"
        self.description = "Autonomous backend refactor and hardening agent for production-grade applications"
        self.version = "1.0.0"
        self.capabilities = self._get_capabilities()
    
    def _get_capabilities(self) -> Dict[str, any]:
        """Define agent capabilities for VSCode"""
        return {
            "refactoring": {
                "autonomous": True,
                "interactive": True,
                "guided": True,
                "supports_languages": ["python", "javascript", "typescript", "go"],
                "supports_frameworks": ["fastapi", "django", "express", "nestjs", "gin", "echo"]
            },
            "research": {
                "web_research": True,
                "documentation_analysis": True,
                "best_practices": True,
                "authoritative_sources": True
            },
            "architecture": {
                "hexagonal_architecture": True,
                "error_handling": "rfc9457",
                "input_validation": True,
                "observability": True,
                "reliability_patterns": True
            },
            "security": {
                "owasp_compliance": True,
                "secret_management": True,
                "pii_handling": True,
                "vulnerability_scanning": True
            },
            "progress_tracking": {
                "real_time_updates": True,
                "task_breakdown": True,
                "rollback_support": True,
                "validation_steps": True
            }
        }
    
    def get_agent_manifest(self) -> Dict[str, any]:
        """Generate agent manifest for VSCode registration"""
        return {
            "id": self.agent_id,
            "name": self.display_name,
            "description": self.description,
            "version": self.version,
            "capabilities": self.capabilities,
            "configuration": {
                "autonomy_levels": ["full", "interactive", "guided"],
                "risk_tolerance": ["low", "medium", "high"],
                "stack_preferences": [
                    "lovable-supabase-github",
                    "python-fastapi", 
                    "node-express",
                    "go-gin",
                    "auto-detect"
                ]
            },
            "commands": [
                {
                    "id": "metapod.refactor",
                    "title": "Start Autonomous Refactoring",
                    "description": "Begin autonomous backend refactoring with Metapod",
                    "icon": "tools"
                },
                {
                    "id": "metapod.research",
                    "title": "Research Best Practices", 
                    "description": "Research current best practices for a topic",
                    "icon": "search"
                },
                {
                    "id": "metapod.status",
                    "title": "Show Progress Status",
                    "description": "Display current refactoring progress",
                    "icon": "checklist"
                }
            ],
            "activation_events": [
                "onLanguage:python",
                "onLanguage:javascript", 
                "onLanguage:typescript",
                "onLanguage:go"
            ]
        }
    
    async def handle_vscode_request(self, request: Dict[str, any]) -> Dict[str, any]:
        """Handle requests from VSCode agent framework"""
        command = request.get("command")
        params = request.get("params", {})
        
        if command == "refactor":
            return await self._handle_refactor_request(params)
        elif command == "research":
            return await self._handle_research_request(params)
        elif command == "status":
            return await self._handle_status_request(params)
        elif command == "get_capabilities":
            return {"capabilities": self.capabilities}
        else:
            return {"error": f"Unknown command: {command}"}
    
    async def _handle_refactor_request(self, params: Dict[str, any]) -> Dict[str, any]:
        """Handle refactoring request from VSCode"""
        project_path = params.get("project_path")
        request_text = params.get("request", "Begin autonomous refactoring")
        autonomy_level = params.get("autonomy_level", "interactive")
        
        if not project_path:
            return {"error": "project_path is required"}
        
        try:
            # Initialize Metapod agent
            agent = MetapodAgent(project_path)
            
            # Execute refactoring
            result = await agent.run(request_text)
            
            return {
                "success": True,
                "result": result,
                "todo_status": agent.get_todo_status(),
                "session_id": f"metapod_{int(time.time())}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "details": "Refactoring failed - check Metapod output for details"
            }
    
    async def _handle_research_request(self, params: Dict[str, any]) -> Dict[str, any]:
        """Handle research request from VSCode"""
        topic = params.get("topic")
        
        if not topic:
            return {"error": "topic is required"}
        
        try:
            # Perform research using Metapod research module
            from research import WebResearcher
            
            async with WebResearcher() as researcher:
                result = await researcher.research_topic(topic)
                
                return {
                    "success": True,
                    "topic": topic,
                    "summary": result.summary,
                    "sources": result.sources,
                    "confidence": result.confidence
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "details": "Research failed - check network connection and dependencies"
            }
    
    async def _handle_status_request(self, params: Dict[str, any]) -> Dict[str, any]:
        """Handle status request from VSCode"""
        session_id = params.get("session_id")
        
        # For now, return a placeholder status
        # In a full implementation, this would track active sessions
        return {
            "success": True,
            "status": "No active session",
            "sessions": []
        }


def register_with_vscode():
    """Register Metapod as a VSCode agent"""
    adapter = VSCodeAgentAdapter()
    manifest = adapter.get_agent_manifest()
    
    # Try to find VSCode agent registry
    vscode_extensions_path = None
    possible_paths = [
        os.path.expanduser("~/.vscode/extensions"),
        os.path.expanduser("~/.vscode-insiders/extensions"),
        "/Applications/Visual Studio Code.app/Contents/Resources/app/extensions"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            vscode_extensions_path = path
            break
    
    if not vscode_extensions_path:
        print("❌ VSCode extensions directory not found")
        return False
    
    # Create agent registration file
    agent_registry_path = Path(vscode_extensions_path) / "metapod-agent"
    agent_registry_path.mkdir(exist_ok=True)
    
    manifest_file = agent_registry_path / "agent-manifest.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Metapod agent registered at: {manifest_file}")
    return True


def create_vscode_task_definition():
    """Create VSCode task definition for Metapod"""
    return {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Metapod: Autonomous Refactor",
                "type": "shell",
                "command": "python3",
                "args": ["${workspaceFolder}/../cli.py", "${workspaceFolder}", "Begin autonomous refactoring"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared",
                    "showReuseMessage": True,
                    "clear": False
                },
                "problemMatcher": []
            },
            {
                "label": "Metapod: Interactive Mode",
                "type": "shell", 
                "command": "python3",
                "args": ["${workspaceFolder}/../cli.py", "${workspaceFolder}", "--interactive"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": True,
                    "panel": "shared"
                }
            },
            {
                "label": "Metapod: Research",
                "type": "shell",
                "command": "python3", 
                "args": ["${workspaceFolder}/../cli.py", "${workspaceFolder}", "--interactive"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": True,
                    "panel": "shared"
                }
            }
        ]
    }


def create_vscode_launch_configuration():
    """Create VSCode launch configuration for debugging Metapod"""
    return {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Debug Metapod Agent",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/cli.py",
                "args": ["${workspaceFolder}", "--verbose", "Debug refactoring session"],
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}",
                "env": {
                    "PYTHONPATH": "${workspaceFolder}"
                }
            }
        ]
    }


if __name__ == "__main__":
    import time
    
    print("🔧 Setting up Metapod as VSCode Agent...")
    
    if register_with_vscode():
        print("✅ Metapod is now available as a VSCode agent!")
        print("\nTo use Metapod in VSCode:")
        print("1. Open VSCode")
        print("2. Open a project folder")
        print("3. Press Ctrl+Shift+P")
        print("4. Type 'Metapod' to see available commands")
        print("\nOr install the full VSCode extension from the marketplace.")
    else:
        print("❌ Failed to register Metapod as VSCode agent")
        print("Consider installing the VSCode extension manually.")
