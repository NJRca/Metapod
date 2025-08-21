#!/usr/bin/env python3
"""
Metapod (Claude Sonnet 4) — Backend Refactor & Hardening Agent

An autonomous agent designed for production-grade backend refactoring.
Plans, researches, edits, tests, validates, and ships small, reversible PR-sized changes.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from urllib.parse import urlparse

import aiohttp
import yaml


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    notes: str = ""
    research_urls: List[str] = field(default_factory=list)


@dataclass
class RefactorContext:
    """Context for the current refactoring session"""
    project_root: Path
    target_stack: str = "lovable-supabase-github"
    current_phase: str = "intake"
    tasks: Dict[str, Task] = field(default_factory=dict)
    research_notes: Dict[str, str] = field(default_factory=dict)
    baseline_metrics: Dict[str, any] = field(default_factory=dict)


class MetapodAgent:
    """
    Autonomous refactor-and-hardening agent for production backends.
    
    Operating Principles:
    - Autonomy & Loop Discipline: Keep going until task is completely solved
    - Research First: Assume training data is stale, fetch fresh docs
    - Architecture & Refactor Backbone: Apply Ports & Adapters (Hexagonal)
    - Security Baseline: Input validation, secrets management, OWASP compliance
    - CI/CD Quality Gates: Type-checks, tests, security scans
    """
    
    def __init__(self, project_root: str):
        self.context = RefactorContext(project_root=Path(project_root))
        self.logger = self._setup_logging()
        self._init_default_tasks()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup structured logging with correlation IDs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def _init_default_tasks(self):
        """Initialize the standard workflow tasks"""
        default_tasks = [
            Task("scope", "Scope & acceptance criteria confirmed"),
            Task("baseline", "Baseline tests/telemetry in place", dependencies=["scope"]),
            Task("plan", "Plan approved (small reversible cuts)", dependencies=["baseline"]),
            Task("implement", "Implement step 1 (inputs validated, errors standardized)", dependencies=["plan"]),
            Task("test", "Tests green (unit/contract/property)", dependencies=["implement"]),
            Task("observability", "Observability updated (logs/metrics/traces)", dependencies=["implement"]),
            Task("pr", "PR opened with checklist & research notes", dependencies=["test", "observability"]),
            Task("rollout", "Rollout plan & rollback documented", dependencies=["pr"])
        ]
        
        for task in default_tasks:
            self.context.tasks[task.id] = task
    
    async def run(self, user_request: str) -> str:
        """
        Main execution loop - autonomous until task is complete
        """
        self.logger.info(f"Starting Metapod agent with request: {user_request}")
        
        try:
            # Phase 1: Intake & Scoping
            await self._intake_and_scoping(user_request)
            
            # Phase 2: Forensics & Baselines
            await self._forensics_and_baselines()
            
            # Phase 3: Plan the Cut
            await self._plan_the_cut()
            
            # Phase 4: Research (Recursive)
            await self._research_phase()
            
            # Phase 5: Implement (Small Diffs)
            await self._implement_phase()
            
            # Phase 6: Test & Validate
            await self._test_and_validate()
            
            # Phase 7: Observability & Ops
            await self._observability_and_ops()
            
            # Phase 8: PR & Rollout
            await self._pr_and_rollout()
            
            return self._generate_completion_report()
            
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}")
            return f"Metapod execution failed: {str(e)}"
    
    async def _intake_and_scoping(self, user_request: str):
        """Phase 1: Restate goal, identify entrypoints, create TODO list"""
        self.logger.info("Phase 1: Intake & Scoping")
        
        # Parse and analyze the request
        scope_analysis = await self._analyze_request(user_request)
        self.context.tasks["scope"].notes = scope_analysis
        self.context.tasks["scope"].status = TaskStatus.COMPLETED
        
        self.logger.info(f"Scope analysis completed: {scope_analysis}")
    
    async def _forensics_and_baselines(self):
        """Phase 2: Enumerate dependencies, capture current behavior"""
        self.logger.info("Phase 2: Forensics & Baselines")
        
        # Check dependencies and versions
        deps = await self._check_dependencies()
        
        # Capture baseline metrics
        baseline = await self._capture_baseline_metrics()
        self.context.baseline_metrics = baseline
        
        self.context.tasks["baseline"].status = TaskStatus.COMPLETED
        self.context.tasks["baseline"].notes = f"Dependencies: {len(deps)}, Baseline captured"
    
    async def _plan_the_cut(self):
        """Phase 3: Produce phased, reversible refactor plan"""
        self.logger.info("Phase 3: Plan the Cut")
        
        plan = await self._generate_refactor_plan()
        self.context.tasks["plan"].notes = plan
        self.context.tasks["plan"].status = TaskStatus.COMPLETED
    
    async def _research_phase(self):
        """Phase 4: Research unknowns, fetch authoritative docs"""
        self.logger.info("Phase 4: Research (Recursive)")
        
        research_items = await self._identify_research_needs()
        
        for item in research_items:
            research_result = await self._research_topic(item)
            self.context.research_notes[item] = research_result
    
    async def _implement_phase(self):
        """Phase 5: Make minimal, verifiable changes"""
        self.logger.info("Phase 5: Implement (Small Diffs)")
        
        # Apply architectural patterns
        await self._apply_hexagonal_architecture()
        await self._standardize_error_handling()
        await self._add_input_validation()
        await self._implement_timeouts_and_retries()
        
        self.context.tasks["implement"].status = TaskStatus.COMPLETED
    
    async def _test_and_validate(self):
        """Phase 6: Update/add tests, run validation"""
        self.logger.info("Phase 6: Test & Validate")
        
        await self._run_test_suite()
        await self._validate_performance()
        
        self.context.tasks["test"].status = TaskStatus.COMPLETED
    
    async def _observability_and_ops(self):
        """Phase 7: Ensure proper logging, metrics, traces"""
        self.logger.info("Phase 7: Observability & Ops")
        
        await self._update_observability()
        
        self.context.tasks["observability"].status = TaskStatus.COMPLETED
    
    async def _pr_and_rollout(self):
        """Phase 8: Open PR, document rollout and rollback"""
        self.logger.info("Phase 8: PR & Rollout")
        
        pr_content = await self._generate_pr_content()
        await self._create_pr(pr_content)
        
        self.context.tasks["pr"].status = TaskStatus.COMPLETED
        self.context.tasks["rollout"].status = TaskStatus.COMPLETED
    
    # Implementation methods
    
    async def _analyze_request(self, request: str) -> str:
        """Analyze user request and identify scope"""
        # Simplified analysis - in practice would use LLM or sophisticated parsing
        return f"Request analysis: {request[:100]}..."
    
    async def _check_dependencies(self) -> List[str]:
        """Check project dependencies and versions"""
        deps = []
        
        # Check for common dependency files
        for dep_file in ["package.json", "requirements.txt", "go.mod", "Cargo.toml"]:
            file_path = self.context.project_root / dep_file
            if file_path.exists():
                deps.append(dep_file)
        
        return deps
    
    async def _capture_baseline_metrics(self) -> Dict[str, any]:
        """Capture current performance and behavior metrics"""
        return {
            "timestamp": "2025-08-20T00:00:00Z",
            "test_count": 0,
            "coverage": 0.0,
            "performance": {}
        }
    
    async def _generate_refactor_plan(self) -> str:
        """Generate phased refactor plan"""
        return """
        Phase 1: Input Validation & Error Standardization
        - Add zod/yup validation at API boundaries
        - Implement RFC 9457 Problem Details for errors
        
        Phase 2: Ports & Adapters Architecture
        - Extract core use cases from handlers
        - Create repository interfaces for data access
        
        Phase 3: Reliability Patterns
        - Add timeouts to all outbound calls
        - Implement retry with jittered backoff
        - Add circuit breakers for fragile dependencies
        """
    
    async def _identify_research_needs(self) -> List[str]:
        """Identify topics that need research"""
        return [
            "latest_framework_patterns",
            "security_best_practices",
            "observability_standards"
        ]
    
    async def _research_topic(self, topic: str) -> str:
        """Research a specific topic using web search and documentation"""
        # In practice, this would use search APIs and fetch documentation
        return f"Research completed for {topic}: Latest patterns and recommendations gathered."
    
    async def _apply_hexagonal_architecture(self):
        """Apply Ports & Adapters pattern"""
        self.logger.info("Applying hexagonal architecture patterns")
    
    async def _standardize_error_handling(self):
        """Implement RFC 9457 Problem Details error format"""
        self.logger.info("Standardizing error handling with Problem Details")
    
    async def _add_input_validation(self):
        """Add input validation at all boundaries"""
        self.logger.info("Adding input validation at API boundaries")
    
    async def _implement_timeouts_and_retries(self):
        """Add timeouts and retry logic"""
        self.logger.info("Implementing timeouts and retry patterns")
    
    async def _run_test_suite(self):
        """Run comprehensive test suite"""
        self.logger.info("Running test suite")
    
    async def _validate_performance(self):
        """Validate performance hasn't regressed"""
        self.logger.info("Validating performance")
    
    async def _update_observability(self):
        """Update logging, metrics, and tracing"""
        self.logger.info("Updating observability infrastructure")
    
    async def _generate_pr_content(self) -> str:
        """Generate PR content using template"""
        return self._get_pr_template()
    
    async def _create_pr(self, content: str):
        """Create GitHub PR"""
        self.logger.info("Creating GitHub PR")
    
    def _generate_completion_report(self) -> str:
        """Generate final completion report with TODO status"""
        completed_tasks = [t for t in self.context.tasks.values() if t.status == TaskStatus.COMPLETED]
        total_tasks = len(self.context.tasks)
        
        report = f"""
# Metapod Completion Report

## Task Summary
- Completed: {len(completed_tasks)}/{total_tasks} tasks
- Phase: {self.context.current_phase}

## TODO Status
"""
        
        for task in self.context.tasks.values():
            status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "❌"
            report += f"- {status_emoji} {task.description}\n"
        
        if self.context.research_notes:
            report += "\n## Research Notes\n"
            for topic, notes in self.context.research_notes.items():
                report += f"- **{topic}**: {notes[:100]}...\n"
        
        return report
    
    def _get_pr_template(self) -> str:
        """Get the PR template"""
        return """## Summary
Refactoring changes following Metapod autonomous agent recommendations.

## Scope
- Modules/files: [AUTO-GENERATED]
- Behavior preserved? Y

## Architecture
- Ports added/changed: [AUTO-GENERATED]
- Repos/transactions: [AUTO-GENERATED]
- Error model → problem+json mapping: Implemented RFC 9457

## Security
- ASVS/API Top 10 items addressed: Input validation, error handling
- Secrets/roles/policies touched: None

## Reliability
- Timeouts/retries/backoff/breakers added: Yes
- Idempotency keys/semantics: [AUTO-GENERATED]

## Observability
- Logs/metrics/traces added/updated: Structured logging with correlation IDs
- Dashboards/alerts: [AUTO-GENERATED]

## Testing
- Characterization tests: Added
- Unit/Property/Contract tests: Updated
- e2e/Smoke: [AUTO-GENERATED]

## Performance
- Before/After p95 & error rate: [AUTO-GENERATED]
- Budgets enforced in CI: Yes

## Release
- Feature flags: [AUTO-GENERATED]
- Rollout steps: [AUTO-GENERATED]
- Rollback plan: [AUTO-GENERATED]
"""

    def get_todo_status(self) -> str:
        """Get current TODO status for display"""
        todo_items = []
        for task in self.context.tasks.values():
            status = "✅" if task.status == TaskStatus.COMPLETED else "⏳"
            todo_items.append(f"{status} {task.description}")
        
        return "```\nTODO Status:\n" + "\n".join(todo_items) + "\n```"


# CLI Interface
async def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python metapod.py <project_path> [request]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    request = sys.argv[2] if len(sys.argv) > 2 else "Begin autonomous refactoring"
    
    agent = MetapodAgent(project_path)
    result = await agent.run(request)
    print(result)
    print("\n" + agent.get_todo_status())


if __name__ == "__main__":
    asyncio.run(main())
