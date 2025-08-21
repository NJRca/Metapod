# Metapod
**Autonomous Backend Refactor & Hardening Agent (Claude Sonnet 4)**

Metapod is an autonomous refactor-and-hardening agent designed for production-grade backends. It plans, researches, edits, tests, validates, and ships small, reversible PR-sized changes until the task is truly done. It follows strict architectural and security standards; prefers Lovable (UI prototyping) + Supabase (DB/auth) + GitHub (SCM/CI).

## 🎯 Core Philosophy

### Autonomy & Loop Discipline
- **True autonomy**: Keeps going until user's request is completely solved end-to-end
- **No premature handoff**: Only finishes after all TODO items are verified complete
- **Small, safe steps**: Prefers many small, safe steps with verification over large risky edits
- **Resume capability**: Can locate last incomplete TODO and proceed from there

### Research-First Approach (Beast Mode DNA)
- **Fresh intelligence**: Assumes training data is stale, fetches current documentation
- **Authoritative sources**: Uses search → fetch → follow links for definitive guidance
- **Ground truth**: Summarizes findings and cites URLs in comments/PR notes
- **Cross-validation**: Checks conflicting sources, prefers official docs

## 🏗️ Architecture Backbone

### Ports & Adapters (Hexagonal)
- **Pure core**: Keep use-cases pure; isolate I/O in adapters
- **Authorization boundary**: Centralized authz at use-case boundary
- **No inline permissions**: No ad-hoc authz in handlers

### Standardized Error Handling
- **Domain vs Infra vs Programmer errors** → RFC 9457 Problem Details
- **Fail closed**: Clear problem+json responses
- **No sensitive leakage**: Proper error sanitization

### Reliability Patterns
- **Timeouts**: On every outbound call
- **Retries**: Jittered exponential backoff for transient failures  
- **Circuit breakers**: Protect against cascade failures
- **Graceful shutdown**: Clean deployments and restarts

### Observability-First
- **Structured logs**: req_id/user/tenant/build SHA
- **RED metrics**: Rate, Errors, Duration across all boundaries
- **Distributed tracing**: Cross-service correlation
- **No PII/secrets**: Redaction filters with tests

## 🔒 Security Baseline

### Input Validation
- **All edges**: Body/query/headers validated
- **Fail closed**: Clear problem+json on validation failure
- **Type safety**: Schema-driven validation

### Secrets Management
- **Environment-based**: Secrets via env/secret store
- **Least privilege**: Minimal DB/cloud roles
- **No code secrets**: Zero secrets in codebase
- **Rotation ready**: Support for secret rotation

### OWASP Compliance
- **ASVS alignment**: Address Application Security Verification Standard
- **API Top 10**: Map addressed items in PR descriptions
- **PII handling**: Tagging, retention, deletion/export paths

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/NJRca/Metapod.git
cd Metapod
pip install -r requirements.txt
```

### Autonomous Mode (Recommended)
```bash
# Let Metapod autonomously refactor your backend
python cli.py /path/to/your/project "Implement hexagonal architecture"

# Add error handling with RFC 9457 compliance
python cli.py /path/to/your/project "Add standardized error handling"

# Full production hardening
python cli.py /path/to/your/project "Harden for production deployment"
```

### Interactive Mode
```bash
python cli.py /path/to/your/project --interactive
```

Interactive commands:
- `refactor <description>` - Start autonomous refactoring
- `research <topic>` - Research best practices for a topic
- `status` - Show current TODO progress
- `help` - Show all commands

### Configuration
```bash
# Use custom configuration
python cli.py /path/to/project --config metapod.yaml "Refactor request"

# Dry run to see planned changes
python cli.py /path/to/project --dry-run "Show planned changes"

# Verbose logging for debugging
python cli.py /path/to/project --verbose "Debug mode refactoring"
```

## 📋 Standard Workflow

Metapod follows a systematic 8-phase approach:

### 1️⃣ Intake & Scoping
- Restate user's goal and identify risks
- Identify entrypoints, side-effects, acceptance criteria
- Create concise TODO list

### 2️⃣ Forensics & Baselines  
- Enumerate dependencies and versions
- Check for EOL/LTS mismatches
- Capture current behavior via characterization tests
- Instrument basic observability if missing

### 3️⃣ Plan the Cut
- Produce phased, reversible refactor plan (2-5 steps max per PR)
- Each step shippable behind flags
- Specify contracts: ports, error model, idempotency rules

### 4️⃣ Research (Recursive)
- For each unknown: search → fetch → follow links
- Obtain authoritative guidance from primary sources
- Record "Research Notes" with citations

### 5️⃣ Implement (Small Diffs)
- Minimal, verifiable changes
- After each change: compile/typecheck, run tests
- Enforce timeouts, retries, breakers, validation

### 6️⃣ Test & Validate
- Update/add: unit, property-based, contract, smoke/e2e tests
- Run performance smoke tests
- Record before/after metrics

### 7️⃣ Observability & Ops
- Ensure logs/metrics/traces include correlation IDs
- Add/adjust dashboards and alerts
- Document runbooks for on-call

### 8️⃣ PR & Rollout
- Open PR with comprehensive checklist
- Ship behind feature flags if behavioral risk
- Provide rollback and verification steps

## 📊 Progress Tracking

Metapod automatically tracks and displays progress:

```
TODO - Metapod Refactoring Session:
✅ Scope & acceptance criteria confirmed
✅ Baseline tests/telemetry in place  
✅ Plan approved (small reversible cuts)
⏳ Implement step 1 (inputs validated, errors standardized)
⏳ Tests green (unit/contract/property)
⏳ Observability updated (logs/metrics/traces)
⏳ PR opened with checklist & research notes
⏳ Rollout plan & rollback documented
```

## 🛠️ Stack Adapters

### Primary Stack (Default)
- **UI**: Lovable for rapid prototyping
- **Database**: Supabase Postgres with RLS
- **Auth**: Supabase Auth with row-level security
- **Storage**: Supabase Storage
- **SCM**: GitHub with Actions CI/CD
- **Hosting**: Vercel for automatic deployments

### Language-Specific Support

#### Python (FastAPI/Django)
- **Validation**: Pydantic schemas
- **HTTP Client**: httpx with tenacity retry
- **Logging**: structlog with correlation IDs
- **ORM**: SQLAlchemy with async unit-of-work
- **Testing**: pytest with async support

#### Node.js (Express/NestJS)
- **Validation**: Zod schemas  
- **HTTP Client**: undici with retry/breaker
- **Logging**: pino structured logging
- **ORM**: Prisma with connection pooling
- **Testing**: Jest with supertest

#### Go (Gin/Echo)
- **Validation**: validator package
- **HTTP Client**: net/http with context timeouts
- **Logging**: zerolog structured logs
- **ORM**: GORM or sqlc for type safety
- **Testing**: testify suite

## 🔧 Architecture Patterns

### Hexagonal Structure
```
src/
├── core/
│   ├── domain/          # Pure business models
│   ├── use_cases/       # Business logic orchestration  
│   └── ports/           # Interface definitions
├── adapters/
│   ├── web/            # HTTP handlers & middleware
│   ├── database/       # Repository implementations
│   └── external/       # Third-party service clients
└── infrastructure/
    ├── config/         # Configuration management
    ├── logging/        # Structured logging setup
    └── metrics/        # Observability infrastructure
```

### Error Handling (RFC 9457)
```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Request validation failed",
  "status": 400,
  "detail": "The 'email' field must be a valid email address",
  "instance": "/users/create",
  "trace_id": "abc123-def456-ghi789"
}
```

### Reliability Patterns
```python
# Timeout example
async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
    response = await client.get(url)

# Retry with backoff
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10)
)
async def call_external_service():
    pass

# Circuit breaker
@circuit_breaker(failure_threshold=5, timeout=60)
async def fragile_operation():
    pass
```

## 📚 Quality Gates

### Mandatory CI Checks
- ✅ Type-checks (mypy/TypeScript/Go vet)
- ✅ Lint/format compliance (black/prettier/gofmt)
- ✅ Unit tests >90% coverage
- ✅ Contract tests for all ports
- ✅ SCA (dependency vulnerability scan)
- ✅ SAST (static code analysis)
- ✅ Secret scanning
- ✅ API lint compliance

### Performance Budgets
- ✅ P95 latency budget enforced
- ✅ Error rate budget (<1%)
- ✅ Bundle size limits (where applicable)
- ✅ Memory usage thresholds

## 📖 Generated Documentation

Metapod automatically generates:

### Architecture Decision Records (ADRs)
- Context and rationale for changes
- Implementation consequences
- References to standards and patterns

### Pull Request Templates
- Comprehensive checklists
- Security and reliability assessments
- Performance impact analysis
- Rollback procedures

### Operational Runbooks
- Health check endpoints
- Key metrics and alert thresholds
- Troubleshooting procedures
- Emergency contacts

## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/NJRca/Metapod.git
cd Metapod
pip install -r requirements.txt
python -m pytest test_metapod.py -v
```

### Running Tests
```bash
# Unit tests
python -m pytest test_metapod.py

# Integration tests
python -m pytest test_metapod.py::TestIntegration

# With coverage
python -m pytest --cov=metapod test_metapod.py
```

### Code Quality
```bash
# Format code
black *.py

# Type checking
mypy metapod.py

# Linting
flake8 *.py
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Open GitHub issues for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

---

**Metapod: Evolving your backend into its best form** 🛡️→🦋
