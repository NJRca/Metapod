"""
Configuration and rules for Metapod agent
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MetapodConfig:
    """Configuration for Metapod autonomous agent"""
    
    # Stack preferences
    preferred_stack: str = "lovable-supabase-github"
    
    # Architecture rules (enforceable fitness functions)
    architecture_rules: List[str] = None
    
    # Security baseline requirements
    security_requirements: List[str] = None
    
    # CI/CD quality gates
    quality_gates: List[str] = None
    
    # Observability requirements
    observability_requirements: List[str] = None
    
    def __post_init__(self):
        if self.architecture_rules is None:
            self.architecture_rules = [
                "No DB/network I/O outside adapters/repositories",
                "All outbound calls must set timeouts; transient paths must have jittered retry",
                "Every handler validates input and returns RFC 9457 problem+json on 4xx/5xx",
                "All logs are structured and carry a correlation/trace ID",
                "Tests required for every new/changed port (contract tests)",
                "Prohibit secrets and PII in logs; add redaction filter tests",
                "CI must run: typecheck, lint/format, unit, contract, SCA, SAST, secret scan, API lint"
            ]
        
        if self.security_requirements is None:
            self.security_requirements = [
                "Input validation at all edges (body/query/headers)",
                "Fail closed with clear problem+json responses",
                "Secrets via env/secret store, least-privileged DB/cloud roles",
                "No secrets in code",
                "Follow OWASP ASVS & API Top 10",
                "PII tagging, retention, and deletion/export paths",
                "Never log secrets/PII; add redaction filters"
            ]
        
        if self.quality_gates is None:
            self.quality_gates = [
                "Type-checks must pass",
                "Lint/format compliance",
                "Unit tests >90% coverage",
                "Contract tests for all ports",
                "SCA (dependency scan)",
                "SAST (static analysis)",
                "Secret scanning",
                "API lint compliance",
                "Performance budgets enforced",
                "Error rate budget enforced"
            ]
        
        if self.observability_requirements is None:
            self.observability_requirements = [
                "Structured logs with correlation IDs",
                "RED metrics (Rate, Errors, Duration)",
                "Distributed tracing across boundaries",
                "Request/user/tenant/build SHA in logs",
                "Circuit breaker metrics",
                "Database connection pool metrics",
                "Cache hit/miss rates"
            ]


# Stack-specific adapters and configurations
STACK_CONFIGS = {
    "node-express": {
        "validation": "zod",
        "http_client": "undici",
        "logging": "pino",
        "metrics": "prometheus",
        "tracing": "opentelemetry",
        "orm": "prisma",
        "testing": "jest"
    },
    "python-fastapi": {
        "validation": "pydantic",
        "http_client": "httpx",
        "logging": "structlog",
        "metrics": "prometheus",
        "tracing": "opentelemetry",
        "orm": "sqlalchemy",
        "testing": "pytest"
    },
    "go-gin": {
        "validation": "validator",
        "http_client": "net/http",
        "logging": "zerolog",
        "metrics": "prometheus",
        "tracing": "opentelemetry",
        "orm": "gorm",
        "testing": "testify"
    },
    "lovable-supabase-github": {
        "ui": "lovable",
        "database": "supabase-postgres",
        "auth": "supabase-auth",
        "storage": "supabase-storage",
        "scm": "github",
        "ci": "github-actions",
        "hosting": "vercel"
    }
}


class ArchitecturePatterns:
    """Standard architecture patterns and implementations"""
    
    HEXAGONAL_STRUCTURE = {
        "core": ["domain", "use_cases", "ports"],
        "adapters": ["web", "database", "external_services"],
        "infrastructure": ["config", "logging", "metrics", "health"]
    }
    
    ERROR_HANDLING_PATTERNS = {
        "domain_errors": "Business logic violations",
        "infrastructure_errors": "External system failures",
        "programmer_errors": "Code bugs and validation failures"
    }
    
    RELIABILITY_PATTERNS = [
        "timeouts",
        "retries_with_backoff",
        "circuit_breakers",
        "bulkheads",
        "graceful_shutdown",
        "health_checks"
    ]


class SecurityBaseline:
    """Security requirements and patterns"""
    
    OWASP_API_TOP_10 = [
        "Broken Object Level Authorization",
        "Broken User Authentication", 
        "Excessive Data Exposure",
        "Lack of Resources & Rate Limiting",
        "Broken Function Level Authorization",
        "Mass Assignment",
        "Security Misconfiguration",
        "Injection",
        "Improper Assets Management",
        "Insufficient Logging & Monitoring"
    ]
    
    OWASP_ASVS_LEVELS = {
        "level_1": "Basic security controls",
        "level_2": "Standard security controls",
        "level_3": "Advanced security controls"
    }
    
    PII_CATEGORIES = [
        "personal_identifiers",
        "financial_data",
        "health_data",
        "biometric_data",
        "location_data",
        "behavioral_data"
    ]


# Default configuration instance
DEFAULT_CONFIG = MetapodConfig()
