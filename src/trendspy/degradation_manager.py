"""
Graceful Degradation System

Replaces hard circuit breaker with intelligent health-based processing.
Continues operating on high-priority keywords even under rate limiting.

Health States:
- HEALTHY: Normal operation
- DEGRADED_MINOR: Process HIGH and MEDIUM priority keywords
- DEGRADED_MAJOR: Process only HIGH priority keywords
- RECOVERY: Gradual return to normal after degradation
"""

import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HealthState(Enum):
    """System health states for graceful degradation."""

    HEALTHY = "healthy"
    DEGRADED_MINOR = "degraded_minor"
    DEGRADED_MAJOR = "degraded_major"
    RECOVERY = "recovery"


class Priority(Enum):
    """Keyword priority levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DegradationManager:
    """
    Manages system health states and priority-based processing decisions.

    Instead of completely stopping (circuit breaker), intelligently degrades:
    - Minor degradation: Skip low-priority keywords
    - Major degradation: Only process high-priority keywords
    - Recovery: Gradually return to full processing

    Example:
        >>> manager = DegradationManager()
        >>> manager.update_health(got_429=True)
        >>> if manager.should_process_keyword(Priority.HIGH):
        >>>     # Process keyword
    """

    def __init__(
        self,
        minor_threshold: int = 5,
        major_threshold: int = 10,
        recovery_successes: int = 3,
    ):
        """
        Initialize degradation manager.

        Args:
            minor_threshold: Consecutive 429s before minor degradation
            major_threshold: Consecutive 429s before major degradation
            recovery_successes: Consecutive successes to return to healthy
        """
        self.minor_threshold = minor_threshold
        self.major_threshold = major_threshold
        self.recovery_successes = recovery_successes

        self.health_state = HealthState.HEALTHY
        self.consecutive_429s = 0
        self.consecutive_successes = 0

        logger.info(
            f"DegradationManager initialized "
            f"(minor_threshold={minor_threshold}, "
            f"major_threshold={major_threshold})"
        )

    def update_health(self, got_429: bool):
        """
        Update health state based on request result.

        Args:
            got_429: Whether request got 429 error
        """
        if got_429:
            self.consecutive_429s += 1
            self.consecutive_successes = 0

            old_state = self.health_state

            if self.consecutive_429s >= self.major_threshold:
                self.health_state = HealthState.DEGRADED_MAJOR
            elif self.consecutive_429s >= self.minor_threshold:
                self.health_state = HealthState.DEGRADED_MINOR

            if self.health_state != old_state:
                logger.warning(
                    f"Health degraded: {old_state.value} → {self.health_state.value} "
                    f"(consecutive_429s={self.consecutive_429s})"
                )
        else:
            self.consecutive_successes += 1

            # Only reduce 429 counter, don't reset completely
            if self.consecutive_429s > 0:
                self.consecutive_429s = max(0, self.consecutive_429s - 1)

            old_state = self.health_state

            # Return to healthy after enough successes
            if self.consecutive_successes >= self.recovery_successes:
                if self.health_state != HealthState.HEALTHY:
                    self.health_state = HealthState.RECOVERY

                # Full recovery after sustained success
                if self.consecutive_successes >= self.recovery_successes * 2:
                    self.health_state = HealthState.HEALTHY
                    self.consecutive_429s = 0

            if self.health_state != old_state:
                logger.info(
                    f"Health improved: {old_state.value} → {self.health_state.value} "
                    f"(consecutive_successes={self.consecutive_successes})"
                )

    def should_process_keyword(self, keyword_priority: Priority) -> bool:
        """
        Determine if keyword should be processed based on health and priority.

        Args:
            keyword_priority: Priority level of the keyword

        Returns:
            True if should process, False if should skip
        """
        if self.health_state == HealthState.HEALTHY:
            return True

        elif self.health_state == HealthState.RECOVERY:
            return True  # Process all during recovery

        elif self.health_state == HealthState.DEGRADED_MINOR:
            # Skip LOW priority only
            should_process = keyword_priority in [Priority.HIGH, Priority.MEDIUM]
            if not should_process:
                logger.debug(
                    f"Skipping {keyword_priority.value} priority (DEGRADED_MINOR)"
                )
            return should_process

        elif self.health_state == HealthState.DEGRADED_MAJOR:
            # Only HIGH priority
            should_process = keyword_priority == Priority.HIGH
            if not should_process:
                logger.debug(
                    f"Skipping {keyword_priority.value} priority (DEGRADED_MAJOR)"
                )
            return should_process

        return False

    def get_health_status(self) -> dict:
        """
        Get current health status.

        Returns:
            Dict with health state and metrics
        """
        return {
            "health_state": self.health_state.value,
            "consecutive_429s": self.consecutive_429s,
            "consecutive_successes": self.consecutive_successes,
            "processing_all": self.health_state
            in [HealthState.HEALTHY, HealthState.RECOVERY],
        }

    def reset(self):
        """Reset to healthy state."""
        self.health_state = HealthState.HEALTHY
        self.consecutive_429s = 0
        self.consecutive_successes = 0
        logger.info("DegradationManager reset to HEALTHY")
