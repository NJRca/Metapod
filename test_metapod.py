"""
Test suite for Metapod autonomous refactoring agent
"""

import asyncio
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from metapod import MetapodAgent, TaskStatus
from config import DEFAULT_CONFIG
from refactor import RefactorOrchestrator, RefactorStep
from templates import PRTemplate, TODOTemplate


class TestMetapodAgent(unittest.TestCase):
    """Test the main Metapod agent functionality"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.agent = MetapodAgent(self.temp_dir)
    
    def tearDown(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent.context)
        self.assertEqual(self.agent.context.project_root, Path(self.temp_dir))
        self.assertIn("scope", self.agent.context.tasks)
        self.assertIn("baseline", self.agent.context.tasks)
    
    def test_default_tasks_created(self):
        """Test that default workflow tasks are created"""
        expected_tasks = [
            "scope", "baseline", "plan", "implement", 
            "test", "observability", "pr", "rollout"
        ]
        
        for task_id in expected_tasks:
            self.assertIn(task_id, self.agent.context.tasks)
            task = self.agent.context.tasks[task_id]
            self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_todo_status_generation(self):
        """Test TODO status generation"""
        # Mark some tasks as completed
        self.agent.context.tasks["scope"].status = TaskStatus.COMPLETED
        self.agent.context.tasks["baseline"].status = TaskStatus.COMPLETED
        
        todo_status = self.agent.get_todo_status()
        
        self.assertIn("✅", todo_status)  # Should have completed tasks
        self.assertIn("⏳", todo_status)  # Should have pending tasks
        self.assertIn("TODO Status:", todo_status)
    
    @pytest.mark.asyncio
    async def test_intake_and_scoping(self):
        """Test intake and scoping phase"""
        request = "Implement hexagonal architecture"
        
        await self.agent._intake_and_scoping(request)
        
        scope_task = self.agent.context.tasks["scope"]
        self.assertEqual(scope_task.status, TaskStatus.COMPLETED)
        self.assertIn("Request analysis", scope_task.notes)
    
    @pytest.mark.asyncio 
    async def test_forensics_and_baselines(self):
        """Test forensics and baseline capture"""
        await self.agent._forensics_and_baselines()
        
        baseline_task = self.agent.context.tasks["baseline"]
        self.assertEqual(baseline_task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(self.agent.context.baseline_metrics)


class TestRefactorOrchestrator(unittest.TestCase):
    """Test refactoring orchestration"""
    
    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.orchestrator = RefactorOrchestrator(self.temp_dir, "python")
    
    def tearDown(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @pytest.mark.asyncio
    async def test_generate_refactor_plan(self):
        """Test refactor plan generation"""
        plan = await self.orchestrator.generate_refactor_plan()
        
        self.assertIsInstance(plan, list)
        self.assertTrue(len(plan) > 0)
        
        # Check that all steps are RefactorStep instances
        for step in plan:
            self.assertIsInstance(step, RefactorStep)
            self.assertIsNotNone(step.name)
            self.assertIsNotNone(step.description)
            self.assertIn(step.risk_level, ["low", "medium", "high"])
    
    @pytest.mark.asyncio
    async def test_validate_step(self):
        """Test step validation"""
        step = RefactorStep(
            name="test_step",
            description="Test step",
            files_affected=["test.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Check syntax", "Run tests"]
        )
        
        result = await self.orchestrator.validate_step(step)
        self.assertTrue(result)


class TestTemplates(unittest.TestCase):
    """Test template generation"""
    
    def test_pr_template_generation(self):
        """Test PR template generation"""
        pr_content = PRTemplate.generate(
            summary="Test refactoring",
            modules_affected=["src/main.py"],
            behavior_preserved=True,
            architecture_changes={"ports": "Added user repository port"},
            security_items=["Input validation"],
            reliability_changes=["Added timeouts"],
            observability_updates=["Added structured logging"],
            test_updates=["Added unit tests"],
            performance_data={"coverage_change": "+10%"},
            release_plan={"risk_level": "Low"}
        )
        
        self.assertIn("## Summary", pr_content)
        self.assertIn("Test refactoring", pr_content)
        self.assertIn("src/main.py", pr_content)
        self.assertIn("RFC 9457", pr_content)
    
    def test_todo_template_generation(self):
        """Test TODO template generation"""
        initial_todo = TODOTemplate.generate_initial_todo()
        
        self.assertIn("TODO - Metapod", initial_todo)
        self.assertIn("⏳", initial_todo)
        self.assertIn("Scope & acceptance criteria", initial_todo)
        
        # Test updating TODO
        completed = ["Scope & acceptance criteria confirmed"]
        updated_todo = TODOTemplate.update_todo(completed)
        
        self.assertIn("✅", updated_todo)
        self.assertIn("⏳", updated_todo)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def setUp(self):
        """Setup integration test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a mock Python project
        project_files = [
            "requirements.txt",
            "src/main.py",
            "src/models.py",
            "tests/test_main.py"
        ]
        
        for file_path in project_files:
            full_path = Path(self.temp_dir) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("# Mock file content\n")
    
    def tearDown(self):
        """Cleanup integration test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @pytest.mark.asyncio
    async def test_full_workflow_simulation(self):
        """Test complete workflow simulation"""
        agent = MetapodAgent(self.temp_dir)
        
        # Simulate running through all phases
        await agent._intake_and_scoping("Implement error handling")
        await agent._forensics_and_baselines()
        await agent._plan_the_cut()
        
        # Check that tasks are being marked as completed
        completed_count = sum(
            1 for task in agent.context.tasks.values() 
            if task.status == TaskStatus.COMPLETED
        )
        
        self.assertGreaterEqual(completed_count, 3)
    
    def test_dependency_detection(self):
        """Test dependency file detection"""
        agent = MetapodAgent(self.temp_dir)
        
        # Check that requirements.txt was detected in our mock project
        req_file = Path(self.temp_dir) / "requirements.txt"
        self.assertTrue(req_file.exists())


class TestConfiguration(unittest.TestCase):
    """Test configuration and rules"""
    
    def test_default_config_loaded(self):
        """Test that default configuration loads correctly"""
        self.assertIsNotNone(DEFAULT_CONFIG)
        self.assertIsNotNone(DEFAULT_CONFIG.architecture_rules)
        self.assertIsNotNone(DEFAULT_CONFIG.security_requirements)
        self.assertTrue(len(DEFAULT_CONFIG.architecture_rules) > 0)
    
    def test_architecture_rules_defined(self):
        """Test that architecture rules are properly defined"""
        rules = DEFAULT_CONFIG.architecture_rules
        
        # Check for key rules
        timeout_rule = any("timeout" in rule.lower() for rule in rules)
        validation_rule = any("validation" in rule.lower() for rule in rules)
        logging_rule = any("log" in rule.lower() for rule in rules)
        
        self.assertTrue(timeout_rule)
        self.assertTrue(validation_rule)
        self.assertTrue(logging_rule)


# Test fixtures for async tests
@pytest.fixture
def temp_project():
    """Create a temporary project for testing"""
    temp_dir = tempfile.mkdtemp()
    
    # Create mock project structure
    files = {
        "package.json": '{"name": "test-project"}',
        "src/index.js": "console.log('Hello World');",
        "README.md": "# Test Project"
    }
    
    for file_path, content in files.items():
        full_path = Path(temp_dir) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    yield temp_dir
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_agent_with_mock_project(temp_project):
    """Test agent with a mock project"""
    agent = MetapodAgent(temp_project)
    
    # Test that agent can handle the mock project
    await agent._intake_and_scoping("Add error handling")
    
    scope_task = agent.context.tasks["scope"]
    assert scope_task.status == TaskStatus.COMPLETED


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
