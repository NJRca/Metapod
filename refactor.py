"""
Refactoring patterns and implementations for Metapod agent
"""

import asyncio
import ast
import logging
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from config import ArchitecturePatterns, SecurityBaseline


@dataclass
class RefactorStep:
    """A single refactoring step"""
    name: str
    description: str
    files_affected: List[str]
    risk_level: str  # "low", "medium", "high"
    reversible: bool
    validation_steps: List[str]


class HexagonalArchitectureRefactor:
    """Implements hexagonal architecture refactoring"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
    
    async def apply_hexagonal_structure(self) -> List[RefactorStep]:
        """Apply hexagonal architecture to existing codebase"""
        steps = []
        
        # Step 1: Create directory structure
        steps.append(await self._create_directory_structure())
        
        # Step 2: Extract domain models
        steps.append(await self._extract_domain_models())
        
        # Step 3: Create port interfaces
        steps.append(await self._create_port_interfaces())
        
        # Step 4: Implement adapters
        steps.append(await self._implement_adapters())
        
        # Step 5: Refactor handlers to use cases
        steps.append(await self._refactor_handlers_to_use_cases())
        
        return steps
    
    async def _create_directory_structure(self) -> RefactorStep:
        """Create hexagonal architecture directory structure"""
        directories = [
            "src/core/domain",
            "src/core/use_cases",
            "src/core/ports",
            "src/adapters/web",
            "src/adapters/database",
            "src/adapters/external",
            "src/infrastructure/config",
            "src/infrastructure/logging",
            "src/infrastructure/metrics"
        ]
        
        return RefactorStep(
            name="create_hex_structure",
            description="Create hexagonal architecture directory structure",
            files_affected=[f"{d}/.gitkeep" for d in directories],
            risk_level="low",
            reversible=True,
            validation_steps=["Check directory structure exists", "Verify no existing code broken"]
        )
    
    async def _extract_domain_models(self) -> RefactorStep:
        """Extract domain models from existing code"""
        return RefactorStep(
            name="extract_domain_models",
            description="Extract pure domain models without dependencies",
            files_affected=["src/core/domain/*.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["Domain models have no external dependencies", "Tests still pass"]
        )
    
    async def _create_port_interfaces(self) -> RefactorStep:
        """Create port interfaces for external dependencies"""
        return RefactorStep(
            name="create_port_interfaces",
            description="Define port interfaces for repositories and external services",
            files_affected=["src/core/ports/*.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Interfaces are properly defined", "No implementation details in ports"]
        )
    
    async def _implement_adapters(self) -> RefactorStep:
        """Implement adapters for ports"""
        return RefactorStep(
            name="implement_adapters",
            description="Implement concrete adapters for each port",
            files_affected=["src/adapters/**/*.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["All ports have implementations", "Adapters pass contract tests"]
        )
    
    async def _refactor_handlers_to_use_cases(self) -> RefactorStep:
        """Refactor HTTP handlers to use core use cases"""
        return RefactorStep(
            name="refactor_handlers",
            description="Move business logic from handlers to use cases",
            files_affected=["src/adapters/web/*.py", "src/core/use_cases/*.py"],
            risk_level="high",
            reversible=True,
            validation_steps=["Handlers only handle HTTP concerns", "Business logic in use cases", "All tests pass"]
        )


class ErrorHandlingRefactor:
    """Implements standardized error handling patterns"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
    
    async def implement_rfc9457_errors(self) -> List[RefactorStep]:
        """Implement RFC 9457 Problem Details for HTTP APIs"""
        steps = []
        
        # Step 1: Create error models
        steps.append(await self._create_error_models())
        
        # Step 2: Create error middleware
        steps.append(await self._create_error_middleware())
        
        # Step 3: Update handlers to use standard errors
        steps.append(await self._update_handlers_error_handling())
        
        return steps
    
    async def _create_error_models(self) -> RefactorStep:
        """Create standardized error models"""
        return RefactorStep(
            name="create_error_models",
            description="Create RFC 9457 Problem Details error models",
            files_affected=["src/core/domain/errors.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Error models follow RFC 9457", "Models are properly typed"]
        )
    
    async def _create_error_middleware(self) -> RefactorStep:
        """Create global error handling middleware"""
        return RefactorStep(
            name="create_error_middleware",
            description="Create middleware to catch and format all errors",
            files_affected=["src/adapters/web/middleware/error_handler.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["All errors are caught", "Errors follow standard format", "No sensitive data leaked"]
        )
    
    async def _update_handlers_error_handling(self) -> RefactorStep:
        """Update all handlers to use standardized error handling"""
        return RefactorStep(
            name="update_handler_errors",
            description="Update handlers to throw domain-specific errors",
            files_affected=["src/adapters/web/handlers/*.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["Handlers throw typed errors", "Error responses are consistent"]
        )


class ValidationRefactor:
    """Implements input validation at all boundaries"""
    
    def __init__(self, project_root: str, stack_type: str):
        self.project_root = Path(project_root)
        self.stack_type = stack_type
        self.logger = logging.getLogger(__name__)
    
    async def implement_input_validation(self) -> List[RefactorStep]:
        """Implement comprehensive input validation"""
        steps = []
        
        # Step 1: Choose validation library
        steps.append(await self._setup_validation_library())
        
        # Step 2: Create validation schemas
        steps.append(await self._create_validation_schemas())
        
        # Step 3: Add validation middleware
        steps.append(await self._add_validation_middleware())
        
        # Step 4: Update handlers with validation
        steps.append(await self._update_handlers_validation())
        
        return steps
    
    async def _setup_validation_library(self) -> RefactorStep:
        """Setup appropriate validation library for stack"""
        library_map = {
            "python": "pydantic",
            "node": "zod",
            "go": "validator"
        }
        
        return RefactorStep(
            name="setup_validation_library",
            description=f"Setup {library_map.get(self.stack_type, 'appropriate')} validation library",
            files_affected=["requirements.txt", "package.json", "go.mod"],
            risk_level="low",
            reversible=True,
            validation_steps=["Library installed", "Basic validation works"]
        )
    
    async def _create_validation_schemas(self) -> RefactorStep:
        """Create validation schemas for all inputs"""
        return RefactorStep(
            name="create_validation_schemas",
            description="Create validation schemas for request bodies, query params, headers",
            files_affected=["src/adapters/web/schemas/*.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Schemas cover all inputs", "Schemas are properly typed"]
        )
    
    async def _add_validation_middleware(self) -> RefactorStep:
        """Add validation middleware"""
        return RefactorStep(
            name="add_validation_middleware",
            description="Add middleware to validate all incoming requests",
            files_affected=["src/adapters/web/middleware/validation.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["All requests validated", "Validation errors return 400 with details"]
        )
    
    async def _update_handlers_validation(self) -> RefactorStep:
        """Update handlers to use validation"""
        return RefactorStep(
            name="update_handlers_validation",
            description="Update all handlers to use validation schemas",
            files_affected=["src/adapters/web/handlers/*.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["All handlers validate input", "Invalid input rejected cleanly"]
        )


class ObservabilityRefactor:
    """Implements observability patterns"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
    
    async def implement_observability(self) -> List[RefactorStep]:
        """Implement comprehensive observability"""
        steps = []
        
        # Step 1: Setup structured logging
        steps.append(await self._setup_structured_logging())
        
        # Step 2: Add correlation IDs
        steps.append(await self._add_correlation_ids())
        
        # Step 3: Setup metrics
        steps.append(await self._setup_metrics())
        
        # Step 4: Setup distributed tracing
        steps.append(await self._setup_tracing())
        
        return steps
    
    async def _setup_structured_logging(self) -> RefactorStep:
        """Setup structured logging with JSON format"""
        return RefactorStep(
            name="setup_structured_logging",
            description="Implement structured JSON logging",
            files_affected=["src/infrastructure/logging/*.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Logs are JSON formatted", "Log levels work correctly"]
        )
    
    async def _add_correlation_ids(self) -> RefactorStep:
        """Add correlation IDs to all requests"""
        return RefactorStep(
            name="add_correlation_ids",
            description="Add correlation IDs to track requests across services",
            files_affected=["src/adapters/web/middleware/correlation.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["All requests have correlation ID", "IDs propagated in logs"]
        )
    
    async def _setup_metrics(self) -> RefactorStep:
        """Setup RED metrics (Rate, Errors, Duration)"""
        return RefactorStep(
            name="setup_metrics",
            description="Implement RED metrics collection",
            files_affected=["src/infrastructure/metrics/*.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Metrics are collected", "Metrics endpoint available"]
        )
    
    async def _setup_tracing(self) -> RefactorStep:
        """Setup distributed tracing"""
        return RefactorStep(
            name="setup_tracing",
            description="Implement distributed tracing with OpenTelemetry",
            files_affected=["src/infrastructure/tracing/*.py"],
            risk_level="low",
            reversible=True,
            validation_steps=["Traces are generated", "Traces include all operations"]
        )


class ReliabilityRefactor:
    """Implements reliability patterns"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
    
    async def implement_reliability_patterns(self) -> List[RefactorStep]:
        """Implement reliability patterns"""
        steps = []
        
        # Step 1: Add timeouts
        steps.append(await self._add_timeouts())
        
        # Step 2: Add retry logic
        steps.append(await self._add_retry_logic())
        
        # Step 3: Add circuit breakers
        steps.append(await self._add_circuit_breakers())
        
        # Step 4: Add graceful shutdown
        steps.append(await self._add_graceful_shutdown())
        
        return steps
    
    async def _add_timeouts(self) -> RefactorStep:
        """Add timeouts to all outbound calls"""
        return RefactorStep(
            name="add_timeouts",
            description="Add configurable timeouts to all external calls",
            files_affected=["src/adapters/external/*.py", "src/adapters/database/*.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["All external calls have timeouts", "Timeouts are configurable"]
        )
    
    async def _add_retry_logic(self) -> RefactorStep:
        """Add retry logic with exponential backoff"""
        return RefactorStep(
            name="add_retry_logic",
            description="Add retry logic with jittered exponential backoff",
            files_affected=["src/infrastructure/reliability/*.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["Retries work for transient failures", "Backoff prevents thundering herd"]
        )
    
    async def _add_circuit_breakers(self) -> RefactorStep:
        """Add circuit breakers for external dependencies"""
        return RefactorStep(
            name="add_circuit_breakers",
            description="Add circuit breakers to prevent cascade failures",
            files_affected=["src/infrastructure/reliability/circuit_breaker.py"],
            risk_level="high",
            reversible=True,
            validation_steps=["Circuit breakers protect against failures", "Breakers have monitoring"]
        )
    
    async def _add_graceful_shutdown(self) -> RefactorStep:
        """Add graceful shutdown handling"""
        return RefactorStep(
            name="add_graceful_shutdown",
            description="Implement graceful shutdown for clean deployments",
            files_affected=["src/main.py", "src/infrastructure/shutdown.py"],
            risk_level="medium",
            reversible=True,
            validation_steps=["Application shuts down cleanly", "In-flight requests completed"]
        )


class RefactorOrchestrator:
    """Orchestrates the complete refactoring process"""
    
    def __init__(self, project_root: str, stack_type: str = "python"):
        self.project_root = project_root
        self.stack_type = stack_type
        self.logger = logging.getLogger(__name__)
        
        # Initialize refactorers
        self.hex_refactor = HexagonalArchitectureRefactor(project_root)
        self.error_refactor = ErrorHandlingRefactor(project_root)
        self.validation_refactor = ValidationRefactor(project_root, stack_type)
        self.observability_refactor = ObservabilityRefactor(project_root)
        self.reliability_refactor = ReliabilityRefactor(project_root)
    
    async def generate_refactor_plan(self) -> List[RefactorStep]:
        """Generate complete refactoring plan"""
        all_steps = []
        
        # Phase 1: Architecture
        hex_steps = await self.hex_refactor.apply_hexagonal_structure()
        all_steps.extend(hex_steps)
        
        # Phase 2: Error Handling
        error_steps = await self.error_refactor.implement_rfc9457_errors()
        all_steps.extend(error_steps)
        
        # Phase 3: Validation
        validation_steps = await self.validation_refactor.implement_input_validation()
        all_steps.extend(validation_steps)
        
        # Phase 4: Observability
        observability_steps = await self.observability_refactor.implement_observability()
        all_steps.extend(observability_steps)
        
        # Phase 5: Reliability
        reliability_steps = await self.reliability_refactor.implement_reliability_patterns()
        all_steps.extend(reliability_steps)
        
        return all_steps
    
    async def validate_step(self, step: RefactorStep) -> bool:
        """Validate a refactoring step"""
        self.logger.info(f"Validating step: {step.name}")
        
        for validation in step.validation_steps:
            # In practice, this would run actual validation logic
            self.logger.info(f"Validation: {validation}")
        
        return True
    
    async def execute_step(self, step: RefactorStep) -> bool:
        """Execute a refactoring step"""
        self.logger.info(f"Executing step: {step.name}")
        
        try:
            # In practice, this would contain the actual refactoring logic
            # For now, we'll simulate execution
            await asyncio.sleep(0.1)  # Simulate work
            
            # Validate the step after execution
            return await self.validate_step(step)
            
        except Exception as e:
            self.logger.error(f"Step {step.name} failed: {e}")
            return False
