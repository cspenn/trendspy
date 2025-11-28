"""
Metrics Collection and Dashboard

This module provides real-time metrics collection and visualization for
monitoring Google Trends API performance.

Key metrics tracked:
- Total requests
- Success rate
- 429 errors
- Response times (avg, min, max, p95)
- Current delay settings
- Consecutive failures

Provides terminal dashboard for live monitoring during execution.
"""

import time
import logging
from typing import Dict, Optional, Deque, cast
from collections import deque
import statistics

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collects and reports performance metrics for Google Trends API calls.

    Tracks success rates, response times, error counts, and provides
    a real-time terminal dashboard.

    Example:
        >>> metrics = MetricsCollector()
        >>> metrics.record_request(success=True, response_time=1.5, status_code=200)
        >>> metrics.print_dashboard()
    """

    def __init__(self, window_size: int = 100):
        """
        Initialize metrics collector.

        Args:
            window_size: Number of recent requests to track for rolling stats
        """
        self.window_size = window_size

        # Core metrics
        response_times: Deque[float] = deque(maxlen=window_size)
        status_codes: Deque[int] = deque(maxlen=window_size)

        self.metrics: Dict = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_429": 0,
            "requests_failed": 0,
            "response_times": response_times,
            "status_codes": status_codes,
            "current_delay": 15.0,
            "consecutive_failures": 0,
            "emergency_mode": False,
        }

        # Timestamps
        self.start_time: float = time.time()
        self.last_request_time: Optional[float] = None
        self.last_success_time: Optional[float] = None
        self.last_failure_time: Optional[float] = None

        # Historical tracking
        self.hourly_requests: Deque[int] = deque(maxlen=60)  # Track requests per minute
        self.hourly_timestamps: Deque[float] = deque(maxlen=60)

        logger.info("MetricsCollector initialized")

    def record_request(
        self,
        success: bool,
        response_time: float,
        status_code: int,
        current_delay: Optional[float] = None,
        consecutive_failures: int = 0,
        emergency_mode: bool = False,
    ):
        """
        Record metrics for a single request.

        Args:
            success: Whether request succeeded (200 OK)
            response_time: Time taken for request in seconds
            status_code: HTTP status code
            current_delay: Current delay setting (optional)
            consecutive_failures: Number of consecutive failures
            emergency_mode: Whether in emergency mode
        """
        self.metrics["requests_total"] += 1

        if success:
            self.metrics["requests_success"] += 1
            self.last_success_time = time.time()
        else:
            self.metrics["requests_failed"] += 1
            self.last_failure_time = time.time()

        if status_code == 429:
            self.metrics["requests_429"] += 1

        self.metrics["response_times"].append(response_time)
        self.metrics["status_codes"].append(status_code)

        if current_delay is not None:
            self.metrics["current_delay"] = current_delay

        self.metrics["consecutive_failures"] = consecutive_failures
        self.metrics["emergency_mode"] = emergency_mode

        self.last_request_time = time.time()

        # Track for hourly rate
        current_minute = int(time.time() / 60)
        if not self.hourly_timestamps or self.hourly_timestamps[-1] != current_minute:
            self.hourly_timestamps.append(current_minute)
            self.hourly_requests.append(1)
        else:
            self.hourly_requests[-1] += 1

    def get_success_rate(self) -> float:
        """
        Calculate success rate percentage.

        Returns:
            Success rate (0-100)
        """
        if self.metrics["requests_total"] == 0:
            return 0.0

        return (self.metrics["requests_success"] / self.metrics["requests_total"]) * 100

    def get_avg_response_time(self) -> float:
        """
        Calculate average response time.

        Returns:
            Average response time in seconds, or 0 if no data
        """
        if not self.metrics["response_times"]:
            return 0.0

        return statistics.mean(self.metrics["response_times"])

    def get_p95_response_time(self) -> float:
        """
        Calculate 95th percentile response time.

        Returns:
            P95 response time in seconds, or 0 if no data
        """
        if not self.metrics["response_times"]:
            return 0.0

        sorted_times = sorted(self.metrics["response_times"])
        index = int(len(sorted_times) * 0.95)
        return sorted_times[index] if index < len(sorted_times) else sorted_times[-1]

    def get_requests_per_hour(self) -> float:
        """
        Estimate current requests per hour rate.

        Returns:
            Estimated requests per hour
        """
        if len(self.hourly_requests) < 2:
            return 0.0

        # Sum requests from last N minutes and extrapolate
        recent_requests = sum(list(self.hourly_requests)[-10:])  # Last 10 minutes
        minutes_tracked = min(10, len(self.hourly_requests))

        if minutes_tracked == 0:
            return 0.0

        requests_per_minute = recent_requests / minutes_tracked
        return requests_per_minute * 60

    def get_runtime(self) -> float:
        """
        Get total runtime in seconds.

        Returns:
            Runtime in seconds
        """
        return time.time() - self.start_time

    def print_dashboard(self):
        """
        Print terminal dashboard with current metrics.

        Displays:
        - Success rate
        - Total requests
        - 429 errors
        - Response time stats
        - Current delay
        - Emergency mode status
        - Requests per hour
        - Runtime
        """
        runtime = self.get_runtime()
        success_rate = self.get_success_rate()
        avg_response = self.get_avg_response_time()
        p95_response = self.get_p95_response_time()
        req_per_hour = self.get_requests_per_hour()

        # Status indicator
        if success_rate >= 95:
            status = "🟢 EXCELLENT"
        elif success_rate >= 85:
            status = "🟡 GOOD"
        elif success_rate >= 70:
            status = "🟠 DEGRADED"
        else:
            status = "🔴 CRITICAL"

        # Emergency mode indicator
        emergency = "🚨 EMERGENCY" if self.metrics["emergency_mode"] else "✓ Normal"

        print(f"\n{'='*70}")
        print("GOOGLE TRENDS API - PERFORMANCE DASHBOARD")
        print(f"{'='*70}")
        print(f"Status: {status}               Emergency Mode: {emergency}")
        print(f"{'-'*70}")
        print(f"Success Rate:        {success_rate:6.2f}%")
        print(f"Total Requests:      {self.metrics['requests_total']:6d}")
        print(f"  ├─ Successful:     {self.metrics['requests_success']:6d}")
        print(f"  ├─ Failed:         {self.metrics['requests_failed']:6d}")
        print(f"  └─ 429 Errors:     {self.metrics['requests_429']:6d}")
        print(f"{'-'*70}")
        print("Response Times:")
        print(f"  ├─ Average:        {avg_response:6.2f}s")
        print(f"  └─ 95th %ile:      {p95_response:6.2f}s")
        print(f"{'-'*70}")
        print("Rate Limiting:")
        print(f"  ├─ Current Delay:  {self.metrics['current_delay']:6.2f}s")
        print(f"  ├─ Consec Fails:   {self.metrics['consecutive_failures']:6d}")
        print(f"  └─ Requests/Hour:  {req_per_hour:6.1f}")
        print(f"{'-'*70}")
        print(f"Runtime:             {runtime/60:6.2f} minutes")
        print(f"{'='*70}\n")

    def get_summary(self) -> Dict:
        """
        Get metrics summary as dictionary.

        Returns:
            Dict with all key metrics
        """
        return {
            "success_rate": self.get_success_rate(),
            "total_requests": self.metrics["requests_total"],
            "successful_requests": self.metrics["requests_success"],
            "failed_requests": self.metrics["requests_failed"],
            "error_429_count": self.metrics["requests_429"],
            "avg_response_time": self.get_avg_response_time(),
            "p95_response_time": self.get_p95_response_time(),
            "current_delay": self.metrics["current_delay"],
            "consecutive_failures": self.metrics["consecutive_failures"],
            "emergency_mode": self.metrics["emergency_mode"],
            "requests_per_hour": self.get_requests_per_hour(),
            "runtime_seconds": self.get_runtime(),
        }

    def reset(self):
        """Reset all metrics (useful for testing or new runs)."""
        self.__init__(window_size=self.window_size)
        logger.info("Metrics reset")
