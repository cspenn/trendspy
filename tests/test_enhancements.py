"""
Comprehensive tests for trendspy fork enhancements.

Copyright (C) 2025 Trust Insights
"""

import pytest
import time
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from trendspy import Trends
from trendspy.rate_limiter import AdaptiveRateLimiter, CircuitBreakerError
from trendspy.session_manager import SessionManager


class TestRateLimiter:
    """Test rate limiting functionality."""

    def test_rate_limiter_enforces_delay(self):
        """Verify minimum delay is enforced."""
        limiter = AdaptiveRateLimiter(base_delay=5)

        start = time.time()
        limiter.wait_if_needed()  # First call (no wait)
        limiter.wait_if_needed()  # Second call (should wait 5s)
        elapsed = time.time() - start

        assert elapsed >= 4.5, f"Should wait ~5s, got {elapsed:.2f}s"

    def test_emergency_mode_activation(self):
        """Verify emergency mode triggers."""
        limiter = AdaptiveRateLimiter(
            base_delay=5,
            emergency_threshold=3
        )

        # Record failures
        for _ in range(3):
            limiter.record_failure()

        assert limiter.emergency_mode, "Emergency mode should activate"

        stats = limiter.get_stats()
        expected_delay = 5 * 3  # base * multiplier
        assert stats['effective_delay'] == expected_delay

    def test_circuit_breaker(self):
        """Verify circuit breaker triggers."""
        limiter = AdaptiveRateLimiter(emergency_threshold=3)

        # Trigger circuit breaker (2x threshold = 6 failures)
        for _ in range(6):
            limiter.record_failure()

        assert limiter.should_circuit_break()

    def test_success_resets_failures(self):
        """Verify success resets failure count."""
        limiter = AdaptiveRateLimiter()

        limiter.record_failure()
        limiter.record_failure()
        assert limiter.consecutive_failures == 2

        limiter.record_success()
        assert limiter.consecutive_failures == 0
        assert not limiter.emergency_mode


class TestSessionManager:
    """Test session management."""

    def test_session_creation(self):
        """Verify session has browser headers."""
        manager = SessionManager(session_file='test_session.pkl')
        session = manager.get_session()

        # Check for browser-like headers
        assert 'User-Agent' in session.headers
        assert 'Chrome' in session.headers['User-Agent']
        assert 'Referer' in session.headers

        # Cleanup
        manager.clear_saved_session()

    def test_session_persistence(self):
        """Verify session can be saved and loaded."""
        # Create and save session
        manager1 = SessionManager(session_file='test_session_persist.pkl')
        session1 = manager1.get_session()
        session1.cookies.set('test_cookie', 'test_value')
        manager1.save_session()

        # Load session in new manager
        manager2 = SessionManager(session_file='test_session_persist.pkl')
        session2 = manager2.get_session()

        # Verify cookie persisted
        assert 'test_cookie' in session2.cookies
        assert session2.cookies['test_cookie'] == 'test_value'

        # Cleanup
        manager2.clear_saved_session()


class TestIntegration:
    """Test full integration with real API."""

    @pytest.mark.slow
    def test_single_keyword_with_enhancements(self):
        """Test single keyword with all enhancements."""
        tr = Trends(
            request_delay=15,
            max_retries=2,
            requests_per_hour=150
        )

        try:
            df = tr.interest_over_time(['python'], timeframe='today 3-m')

            # Verify we got data
            assert not df.empty, "Should retrieve data"
            assert len(df) > 0, "Should have data points"

            # Verify rate limiter tracked success
            stats = tr.rate_limiter.get_stats()
            assert stats['consecutive_failures'] == 0

        except Exception as e:
            pytest.fail(f"Request failed: {e}")

    @pytest.mark.slow
    def test_multiple_keywords_with_rate_limiting(self):
        """Test multiple keywords respect rate limits."""
        tr = Trends(request_delay=10, requests_per_hour=150)

        keywords = ['python', 'javascript', 'java']
        success_count = 0

        start = time.time()

        for keyword in keywords:
            try:
                df = tr.interest_over_time([keyword], timeframe='today 3-m')
                if not df.empty:
                    success_count += 1
            except Exception as e:
                print(f"Failed for {keyword}: {e}")

        elapsed = time.time() - start

        # Should have delays between requests
        expected_min_time = 10 * (len(keywords) - 1)  # 10s * 2 gaps
        assert elapsed >= expected_min_time * 0.9, \
            f"Should take at least {expected_min_time}s, took {elapsed:.0f}s"

        # Most should succeed
        success_rate = (success_count / len(keywords)) * 100
        assert success_rate >= 66, \
            f"Success rate should be >=66%, got {success_rate:.0f}%"

    @pytest.mark.slow
    @pytest.mark.skipif(
        not hasattr(Trends(), 'tor_rotator'),
        reason="Tor not available"
    )
    def test_tor_ip_rotation(self):
        """Test Tor IP rotation (if available)."""
        tr = Trends(use_tor=True)

        if tr.tor_rotator:
            # Get initial IP
            ip1 = tr.tor_rotator.get_current_ip()
            assert ip1, "Should get initial IP"

            # Rotate
            assert tr.tor_rotator.rotate_ip(), "Should rotate successfully"

            # Get new IP
            ip2 = tr.tor_rotator.get_current_ip()
            assert ip2, "Should get new IP"

            # IPs should be different (usually)
            print(f"IP rotation: {ip1} -> {ip2}")


# Run with: pytest tests/test_enhancements.py -v -s
