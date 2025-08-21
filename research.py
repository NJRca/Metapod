"""
Research module for Metapod agent
Handles web research, documentation fetching, and knowledge gathering
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


@dataclass
class ResearchResult:
    """Result of a research query"""
    topic: str
    sources: List[str]
    summary: str
    confidence: float
    last_updated: str


class WebResearcher:
    """Handles web research and documentation fetching"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Metapod-Agent/1.0 (Backend Refactoring Bot)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def research_topic(self, topic: str, sources: List[str] = None) -> ResearchResult:
        """Research a topic using multiple sources"""
        if sources is None:
            sources = await self._find_authoritative_sources(topic)
        
        research_data = []
        for source in sources[:5]:  # Limit to top 5 sources
            try:
                content = await self._fetch_content(source)
                if content:
                    research_data.append({
                        'url': source,
                        'content': content,
                        'relevance': await self._assess_relevance(content, topic)
                    })
            except Exception as e:
                self.logger.warning(f"Failed to fetch {source}: {e}")
        
        summary = await self._synthesize_research(topic, research_data)
        confidence = self._calculate_confidence(research_data)
        
        return ResearchResult(
            topic=topic,
            sources=[item['url'] for item in research_data],
            summary=summary,
            confidence=confidence,
            last_updated="2025-08-20"
        )
    
    async def _find_authoritative_sources(self, topic: str) -> List[str]:
        """Find authoritative sources for a topic"""
        # In a real implementation, this would use search APIs
        source_mappings = {
            "latest_framework_patterns": [
                "https://docs.nestjs.com/",
                "https://fastapi.tiangolo.com/",
                "https://gin-gonic.com/docs/",
                "https://github.com/microsoft/api-guidelines"
            ],
            "security_best_practices": [
                "https://owasp.org/www-project-api-security/",
                "https://cheatsheetseries.owasp.org/",
                "https://github.com/OWASP/ASVS"
            ],
            "observability_standards": [
                "https://opentelemetry.io/docs/",
                "https://prometheus.io/docs/",
                "https://grafana.com/docs/",
                "https://www.elastic.co/guide/"
            ],
            "hexagonal_architecture": [
                "https://alistair.cockburn.us/hexagonal-architecture/",
                "https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html",
                "https://github.com/Sairyss/domain-driven-hexagon"
            ],
            "error_handling_patterns": [
                "https://tools.ietf.org/rfc/rfc9457.txt",
                "https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses"
            ]
        }
        
        return source_mappings.get(topic, [f"https://github.com/search?q={topic}"])
    
    async def _fetch_content(self, url: str) -> Optional[str]:
        """Fetch and clean content from a URL"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text content
                    text = soup.get_text()
                    
                    # Clean up whitespace
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    return text[:10000]  # Limit content size
                    
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    async def _assess_relevance(self, content: str, topic: str) -> float:
        """Assess how relevant content is to the topic"""
        # Simple keyword-based relevance scoring
        topic_words = topic.lower().replace('_', ' ').split()
        content_lower = content.lower()
        
        matches = sum(1 for word in topic_words if word in content_lower)
        return matches / len(topic_words) if topic_words else 0.0
    
    async def _synthesize_research(self, topic: str, research_data: List[Dict]) -> str:
        """Synthesize research into actionable summary"""
        if not research_data:
            return f"No authoritative sources found for {topic}"
        
        # Sort by relevance
        sorted_data = sorted(research_data, key=lambda x: x['relevance'], reverse=True)
        
        summary_parts = [f"Research Summary for {topic}:"]
        
        for i, item in enumerate(sorted_data[:3], 1):
            # Extract key insights (simplified - in practice would use NLP)
            content_preview = item['content'][:500]
            summary_parts.append(f"{i}. From {item['url']}: {content_preview}...")
        
        return "\n\n".join(summary_parts)
    
    def _calculate_confidence(self, research_data: List[Dict]) -> float:
        """Calculate confidence score based on source quality and relevance"""
        if not research_data:
            return 0.0
        
        total_relevance = sum(item['relevance'] for item in research_data)
        avg_relevance = total_relevance / len(research_data)
        
        # Factor in number of sources
        source_factor = min(len(research_data) / 3.0, 1.0)
        
        return avg_relevance * source_factor


class DocumentationAnalyzer:
    """Analyzes project documentation and code patterns"""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.logger = logging.getLogger(__name__)
    
    async def analyze_current_patterns(self) -> Dict[str, any]:
        """Analyze current architectural and code patterns"""
        patterns = {
            "architecture_style": await self._detect_architecture_style(),
            "error_handling": await self._analyze_error_handling(),
            "validation_patterns": await self._analyze_validation(),
            "logging_patterns": await self._analyze_logging(),
            "test_patterns": await self._analyze_test_coverage(),
            "security_patterns": await self._analyze_security_patterns()
        }
        
        return patterns
    
    async def _detect_architecture_style(self) -> str:
        """Detect current architecture style"""
        # Simplified detection logic
        return "layered"  # Would analyze folder structure and imports
    
    async def _analyze_error_handling(self) -> Dict[str, any]:
        """Analyze current error handling patterns"""
        return {
            "has_global_handler": False,
            "uses_standard_format": False,
            "error_types": ["generic", "http"]
        }
    
    async def _analyze_validation(self) -> Dict[str, any]:
        """Analyze input validation patterns"""
        return {
            "validation_library": "none",
            "coverage": "partial",
            "edge_validation": False
        }
    
    async def _analyze_logging(self) -> Dict[str, any]:
        """Analyze logging patterns"""
        return {
            "structured": False,
            "correlation_ids": False,
            "log_level": "info"
        }
    
    async def _analyze_test_coverage(self) -> Dict[str, any]:
        """Analyze test coverage and patterns"""
        return {
            "unit_tests": 0,
            "integration_tests": 0,
            "contract_tests": 0,
            "coverage_percentage": 0.0
        }
    
    async def _analyze_security_patterns(self) -> Dict[str, any]:
        """Analyze security implementation patterns"""
        return {
            "input_validation": "none",
            "auth_patterns": "none",
            "secret_management": "env_vars",
            "owasp_compliance": "unknown"
        }


# Knowledge base for common patterns and solutions
KNOWLEDGE_BASE = {
    "hexagonal_architecture": {
        "description": "Ports and Adapters pattern for clean architecture",
        "benefits": ["Testability", "Framework independence", "Business logic isolation"],
        "implementation": {
            "ports": "Interfaces defining business operations",
            "adapters": "Implementations for external systems",
            "core": "Pure business logic without dependencies"
        }
    },
    "error_handling": {
        "rfc9457": {
            "description": "Problem Details for HTTP APIs",
            "format": {
                "type": "URI identifying the problem type",
                "title": "Human-readable summary",
                "status": "HTTP status code",
                "detail": "Human-readable explanation",
                "instance": "URI identifying specific occurrence"
            }
        }
    },
    "reliability_patterns": {
        "timeout": "Prevent indefinite blocking on external calls",
        "retry": "Handle transient failures with exponential backoff",
        "circuit_breaker": "Prevent cascade failures",
        "bulkhead": "Isolate critical resources"
    }
}
