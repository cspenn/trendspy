"""
Advanced rate limiting for Google Trends.

Copyright (C) 2025 Trust Insights
Based on trendspy (MIT License) by sdil87
https://github.com/sdil87/trendspy

This module extends trendspy with:
- Token bucket + sliding window rate limiting
- Adaptive delay adjustment based on failures
- Circuit breaker pattern for persistent errors
- Request window tracking (hourly quotas)
- Emergency mode with increased delays
- Jitter to prevent thundering herd

License: MIT (see LICENSE file)
"""

import time
import logging
import random
from collections import deque
from datetime import datetime, timedelta
from typing import Deque

logger = logging.getLogger(__name__)


class AdaptiveRateLimiter:
    """
    Sophisticated rate limiter combining multiple strategies.

    Features:
    - Enforces minimum delay between requests
    - Tracks requests per hour (sliding window)
    - Automatic emergency mode on persistent failures
    - Circuit breaker to prevent API hammering
    - Jitter in emergency mode to avoid synchronized retries

    Args:
        requests_per_hour: Maximum requests allowed per hour
        base_delay: Minimum seconds between requests
        emergency_threshold: Consecutive failures before emergency mode
        emergency_multiplier: How much to multiply delays in emergency

    Example:
        >>> limiter = AdaptiveRateLimiter(
        ...     requests_per_hour=150,
        ...     base_delay=15,
        ...     emergency_threshold=5
        ... )
        >>> limiter.wait_if_needed()  # Enforces delays
        >>> limiter.record_success()  # Track outcome
    """

    def __init__(
        self,
        requests_per_hour: int = 200,
        base_delay: float = 15.0,
        emergency_threshold: int = 5,
        emergency_multiplier: int = 3,
    ):
        self.requests_per_hour = requests_per_hour
        self.base_delay = base_delay
        self.emergency_threshold = emergency_threshold
        self.emergency_multiplier = emergency_multiplier

        # Sliding window of request timestamps
        self.request_times: Deque[datetime] = deque(maxlen=requests_per_hour)

        # Circuit breaker state
        self.consecutive_failures = 0
        self.emergency_mode = False
        self.last_request_time: float = 0

        # Phase 1.3: Adaptive delay escalation
        self.delay_multiplier = 1.0

        logger.info(
            f"Initialized AdaptiveRateLimiter: "
            f"{requests_per_hour} req/hr, "
            f"{base_delay}s base delay, "
            f"emergency after {emergency_threshold} failures"
        )

    def wait_if_needed(self) -> None:
        """
        Wait before next request if needed to comply with rate limits.

        Enforces both:
        1. Minimum delay since last request
        2. Maximum requests per hour limit

        Phase 1.2: Applies timing jitter in BOTH normal and emergency modes
        to prevent predictable robot patterns.
        """
        current_time = time.time()

        # Enforce minimum delay since last request
        if self.last_request_time > 0:
            time_since_last = current_time - self.last_request_time

            # Phase 1.3: Calculate effective delay with adaptive multiplier
            effective_delay = self.base_delay * self.delay_multiplier
            if self.emergency_mode:
                effective_delay *= self.emergency_multiplier

            # Phase 1.2: ALWAYS add jitter (not just emergency mode)
            # Normal mode: ±15% jitter, Emergency mode: ±25% jitter
            if self.emergency_mode:
                jitter = random.uniform(0.75, 1.25)  # ±25%
            else:
                jitter = random.uniform(0.85, 1.15)  # ±15%

            effective_delay *= jitter

            # Wait if not enough time has passed
            if time_since_last < effective_delay:
                sleep_time = effective_delay - time_since_last
                logger.debug(
                    f"Rate limit wait: {sleep_time:.2f}s "
                    f"(emergency={self.emergency_mode}, jitter={jitter:.2f}, "
                    f"delay_mult={self.delay_multiplier:.1f})"
                )
                time.sleep(sleep_time)

        # Enforce hourly request limit
        self._enforce_hourly_limit()

        # Record this request
        self.last_request_time = time.time()
        self.request_times.append(datetime.now())

    def _enforce_hourly_limit(self) -> None:
        """
        Ensure we don't exceed hourly request quota.

        Uses sliding window: removes requests older than 1 hour,
        waits if we're at capacity.
        """
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)

        # Remove requests older than 1 hour from window
        while self.request_times and self.request_times[0] < one_hour_ago:
            self.request_times.popleft()

        # If at capacity, wait until oldest request expires
        if len(self.request_times) >= self.requests_per_hour:
            oldest = self.request_times[0]
            wait_until = oldest + timedelta(hours=1)
            wait_seconds = (wait_until - now).total_seconds()

            if wait_seconds > 0:
                logger.warning(
                    f"Hourly limit reached ({self.requests_per_hour} req/hr). "
                    f"Waiting {wait_seconds:.0f}s until quota resets"
                )
                time.sleep(wait_seconds + 1)  # +1 for safety

    def record_success(self) -> None:
        """
        Record a successful request.

        Phase 1.3: Resets failure counter and gradually reduces delay_multiplier.
        Gradual recovery prevents ping-ponging between states.
        """
        if self.consecutive_failures > 0:
            logger.info(
                f"Success after {self.consecutive_failures} failures - "
                f"resetting failure counter"
            )

        self.consecutive_failures = 0

        if self.emergency_mode:
            self.emergency_mode = False
            logger.info("Exiting emergency mode - back to normal operation")

        # Phase 1.3: Gradual recovery of delay multiplier
        if self.delay_multiplier > 1.0:
            old_multiplier = self.delay_multiplier
            self.delay_multiplier = max(1.0, self.delay_multiplier * 0.8)
            logger.info(
                f"Gradual delay recovery: {old_multiplier:.2f}x → {self.delay_multiplier:.2f}x"
            )

    def record_failure(self) -> None:
        """
        Record a failed request (429 rate limit error).

        Phase 1.3: Increments failure counter and IMMEDIATELY escalates delays.
        1st 429: +50% delay, 2nd 429: +100% delay, 3rd+ 429: emergency mode
        """
        self.consecutive_failures += 1

        # Phase 1.3: Immediate adaptive delay escalation
        if self.consecutive_failures == 1:
            self.delay_multiplier = 1.5  # +50%
            logger.warning(
                f"First 429 detected - increasing delays by 50% "
                f"(delay_multiplier={self.delay_multiplier})"
            )
        elif self.consecutive_failures == 2:
            self.delay_multiplier = 2.0  # +100%
            logger.warning(
                f"Second 429 detected - increasing delays by 100% "
                f"(delay_multiplier={self.delay_multiplier})"
            )
        elif self.consecutive_failures >= 3 and not self.emergency_mode:
            self.emergency_mode = True
            self.delay_multiplier = 3.0
            new_delay = (
                self.base_delay * self.delay_multiplier * self.emergency_multiplier
            )

            logger.critical(
                f"EMERGENCY MODE ACTIVATED!\n"
                f"   Consecutive 429s: {self.consecutive_failures}\n"
                f"   Delay multiplier: {self.delay_multiplier}x\n"
                f"   New effective delay: {new_delay:.0f}s (was {self.base_delay:.0f}s)\n"
                f"   This indicates severe rate limiting - proceeding cautiously"
            )

    def should_circuit_break(self) -> bool:
        """
        Check if circuit breaker should trigger.

        Circuit breaker activates after 2x the emergency threshold
        to prevent continued API hammering.

        Returns:
            True if circuit should break (stop all requests)
        """
        threshold = self.emergency_threshold * 2
        should_break = self.consecutive_failures >= threshold

        if should_break:
            logger.critical(
                f"CIRCUIT BREAKER TRIGGERED!\n"
                f"   {self.consecutive_failures} consecutive failures "
                f"(threshold: {threshold})\n"
                f"   Stopping requests to avoid IP blocking"
            )

        return should_break

    def get_stats(self) -> dict:
        """
        Get current rate limiter statistics.

        Returns:
            Dictionary with current state metrics
        """
        # Phase 1.3: Include delay_multiplier in effective delay calculation
        effective_delay = self.base_delay * self.delay_multiplier
        if self.emergency_mode:
            effective_delay *= self.emergency_multiplier

        return {
            "requests_last_hour": len(self.request_times),
            "requests_per_hour_limit": self.requests_per_hour,
            "utilization_pct": (len(self.request_times) / self.requests_per_hour) * 100,
            "consecutive_failures": self.consecutive_failures,
            "emergency_mode": self.emergency_mode,
            "base_delay": self.base_delay,
            "delay_multiplier": self.delay_multiplier,
            "effective_delay": effective_delay,
            "circuit_breaker_threshold": self.emergency_threshold * 2,
        }

    def reset(self) -> None:
        """
        Reset rate limiter state.

        Useful when switching IPs or after long pause.
        """
        self.consecutive_failures = 0
        self.emergency_mode = False
        self.delay_multiplier = 1.0  # Phase 1.3: Reset adaptive multiplier
        self.request_times.clear()
        logger.info("Rate limiter state reset")


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is triggered."""

    pass
