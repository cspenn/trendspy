"""
TrendsPy - A Python library for working with Google Trends.

This library provides a simple and convenient interface for accessing Google Trends data,
allowing you to analyze search trends, get real-time trending topics, and track interest
over time and regions.

Main components:
- Trends: Main client class for accessing Google Trends data
- BatchPeriod: Enum for specifying time periods in batch operations
- TrendKeyword: Class representing a trending search term with metadata
- NewsArticle: Class representing news articles related to trends
- AdaptiveRateLimiter: Advanced rate limiting with emergency mode and circuit breaker
- SessionManager: Session management with cookie persistence
- TorProxyRotator: Free IP rotation using Tor network

Enhanced features (Trust Insights fork):
- Advanced rate limiting with token bucket + sliding window
- Automatic emergency mode on persistent failures
- Circuit breaker pattern to prevent API hammering
- Session persistence across runs
- Optional Tor integration for IP diversity

Project links:
    Homepage: https://github.com/sdil87/trendspy
    Repository: https://github.com/sdil87/trendspy.git
    Issues: https://github.com/sdil87/trendspy/issues
"""

from .client import Trends, BatchPeriod
from .trend_keyword import TrendKeyword, TrendKeywordLite
from .news_article import NewsArticle
from .rate_limiter import AdaptiveRateLimiter, CircuitBreakerError
from .session_manager import SessionManager
from .tor_proxy import TorProxyRotator, create_tor_proxy

__version__ = "0.2.0-enhanced"
__all__ = [
    "Trends",
    "BatchPeriod",
    "TrendKeyword",
    "TrendKeywordLite",
    "NewsArticle",
    "TrendList",
    "AdaptiveRateLimiter",
    "CircuitBreakerError",
    "SessionManager",
    "TorProxyRotator",
    "create_tor_proxy",
]
